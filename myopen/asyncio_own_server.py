import asyncio
import re
import secrets
import logging
import sys

from myopen.open_hmac import (hex_to_message, message_to_hex,
                              sha256_calc_client_response, sha256_calc_kab,
                              sha256_calc_server_response)

# see here :
# https://python-hyper.org/projects/h2/en/stable/asyncio-example.html

ACK = '*#*1##'
SHA2 = '*98*2##'
CMD = '*99*0##'
MON = '*99*1##'

class Server(asyncio.Protocol):
    MODE_SERVER =  0
    MODE_PROXY =   1
    CNX_MODE_CMD = 0
    CNX_MODE_MON = 1

    def __init__(self, password=None, proxy_to_host=None, proxy_to_port=None):
        self.password = password
        self.proxy_to_host = proxy_to_host
        self.proxy_to_port = proxy_to_port
        self.stop = False
        self.mode = self.MODE_SERVER
        if self.proxy_to_host is not None and self.proxy_to_port is not None:
            self.mode = self.MODE_PROXY

        self.server_buffer = ""
        self.client_buffer = ""
        self.handler = None
        self.cnx_mode = ''

    # ------------------------------------------------------------------------
    # 
    # standard protocol interface
    #
    # ------------------------------------------------------------------------

    def connection_made(self, transport):
        self.transport = transport
        self.client = transport.get_extra_info('peername')
        self.log=logging.getLogger('OWNServer_{}_{}'.format(*self.client))
        self.log.debug('connection accepted')
        # prime the thing
        if self.mode == self.MODE_PROXY:
            self.setup_proxy()
        else:
            self.present_server()

    def data_received(self, pkt):
        msg = pkt.decode('ascii')
        self.server_buffer += msg
        # make sure we have a complete data packet and the handler is callable
        # prior to attempting calling the handler (avoids receiving null packets)
        while ('##' in self.server_buffer):
            msg = self.get_packet()
            if (self.handler is not None) and (callable(self.handler)):
                self.handler(msg)

    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')
        self.stop = True
        super().connection_lost(error)

    # ------------------------------------------------------------------------
    # 
    # utilities
    #
    # ------------------------------------------------------------------------

    def send_packet(self, msg):
        self.log.debug('<= %s' % msg)
        pkt = msg.encode('ascii')
        try:
            self.transport.write(pkt)
        except:
            # catch anything that may crash for no reason
            pass

    def get_packet(self):
        pos = self.server_buffer.find('##')
        if pos != -1:
            msg = self.server_buffer[0:pos+2]
            self.server_buffer = self.server_buffer[pos+2:]
            self.log.debug('=> %s' % msg)
            return msg
        return None

    # ------------------------------------------------------------------------
    # 
    # layer 2 handlers
    #
    # ------------------------------------------------------------------------

    async def _setup_proxy(self):
        self.log.debug('initializing client connection to the proxified device')
        self.reader, self.writer = await asyncio.open_connection(self.proxy_to_host, self.proxy_to_port)
        while not self.stop:
            try:
                pkt = await self.reader.readuntil(separator=b'##')
            except Exception as e:
                self.log.debug('got exception %s, closing connection' % (str(e)))
                self.stop = True
                self.transport.close()
            else:
                msg = pkt.decode('ascii')
                self.send_packet(msg)

    def setup_proxy(self):
        self.handler = self.proxy
        # create client connection
        self.log.debug('setting up proxy mode')
        asyncio.ensure_future(self._setup_proxy())

    def proxy(self, msg):
        pkt = msg.encode('ascii')
        self.writer.write(pkt)

    def present_server(self):
        self.handler = self.identify_connection_type
        self.send_packet(ACK)

    def identify_connection_type(self, msg):
        self.cnx_type = msg
        if msg == CMD:
            self.cnx_mode=self.CNX_MODE_CMD
        if msg == MON:
            self.cnx_mode=self.CNX_MODE_MON
        # sha2
        self.handler = self.start_sha2
        self.send_packet(SHA2)

    def start_sha2(self, msg):
        if msg == ACK:
            self.rax = secrets.token_hex(32)
            self.ra = hex_to_message(self.rax)
            self.handler = self.await_sha2_client_response
            self.send_packet('*#%s##' % (self.ra))
        else:
            self.transport.close()

    def await_sha2_client_response(self, msg):
        m = re.match(r'^\*#(?P<rb>\d{128})\*(?P<hmac_client>\d{128})##$', msg)
        if m is not None:
            matches = m.groupdict()
            rb = matches.get('rb', None)
            rbx = message_to_hex(rb)
            hmac_client = matches.get('hmac_client', None)
            kab = sha256_calc_kab(self.password)
            exp_client = sha256_calc_client_response(self.rax, rbx, kab)
            if hmac_client == exp_client:
                hmac_srv = sha256_calc_server_response(self.rax, rbx, kab)
                self.handler = self.await_sha2_client_verify
                self.send_packet('*#%s##' % (hmac_srv))
                return
            else:
                self.log.debug('password fail')
                self.log.debug('exp %s' % (exp_client))
                self.log.debug('got %s' % (hmac_client))
        else:
            self.log.debug('can\'t find matches')
        self.transport.close()

    def await_sha2_client_verify(self, msg):
        if msg == ACK:
            if self.cnx_type == MON:
                self.handler = self.monitor_behavior
            if self.cnx_type == CMD:
                self.handler = self.command_behavior

    def monitor_behavior(self, msg):
        # does nothing
        pass

    def command_behavior(self, msg):
        self.send_packet(ACK)

# ----------------------------------------------------------------------------
# 
# main setup function
#
# ----------------------------------------------------------------------------

def setup_OWN_server(loop, host, port, password, proxy_to_host=None, proxy_to_port=None):
    def start_client_connection():
        return Server(password, proxy_to_host, proxy_to_port)

    ssl_context = None
    coro = loop.create_server(start_client_connection, host, port, ssl=ssl_context)
    asyncio.ensure_future(coro, loop=loop)
