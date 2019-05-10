# -*- coding: utf-8 -*-

import asyncio
import re
from asyncio.streams import StreamReader, StreamWriter
from socket import gaierror

from core.logger import COLOR_LT_BLUE, COLOR_LT_GREEN, COLOR_LT_CYAN, LOG_DEBUG, get_logger
from myopen.asyncio_protocol import OWNProtocol
from myopen.openpass import ownCalcPass
from myopen.open_hmac import ownCalcHmacSha2

__all__ = [
    'MODE_COMMAND', 'MODE_MONITOR',
    'AsyncIOOWNConnection'
]

MODE_COMMAND = 0
MODE_MONITOR = 1
MODE_SUPER_COMMAND = 2


class AsyncIOOWNConnection(object):
    SOCKET_MODES = ('*99*0##', '*99*1##', '*99*9##')
    MODE_COLORS = (COLOR_LT_BLUE, COLOR_LT_GREEN, COLOR_LT_CYAN)
    MODE_NAMES = ('CMD', 'MON', 'SCMD')

    ACK = '*#*1##'

    def __init__(self, host, port, passwd, queue, mode,
                 log=None, loop=None):
        self.host = host
        self.port = port
        self.passwd = passwd
        self.queue = queue
        self.mode = mode
        self.loop = loop
        self._auto_restart = True
        self._run = False
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        self.is_ready = asyncio.Event(loop=self.loop)
        if log is None:
            hdr = '[%s:%d %s]' % \
                (self.host, self.port, self.MODE_NAMES[self.mode])
            self.log = \
                get_logger(header=hdr,
                           color=self.MODE_COLORS[self.mode])
        else:
            self.log = log

    @property
    def auto_restart(self):
        return self._auto_restart

    @auto_restart.setter
    def auto_restart(self, value):
        self._auto_restart = value

    async def run(self):
        self._run = True
        started = False
        # start with the login procedure
        self.reader = StreamReader(loop=self.loop)
        self.protocol = OWNProtocol(self.reader, log=self.log)
        ctr = 0
        while self._run:
            if not self.protocol.is_connected:
                if not self._auto_restart:
                    if started:
                        self.log("no autorestart... bailing out")
                        break
                started = True
                self.log('attempt connection')
                self.is_ready.clear()
                self.log('resetting the msg handler')
                self.msg_handler = self.state_start
                try:
                    self.log('create a new transport connection')
                    self.transport, _ = await self.loop.create_connection(
                        lambda: self.protocol, self.host, self.port)
                except gaierror:
                    self.log('sleep about 5 seconds')
                    await asyncio.sleep(5)
                else:
                    self.log('create a new StreamWriter')
                    self.writer = StreamWriter(
                        self.transport, self.protocol, self.reader, self.loop)
                    self.log('connection is up and running')
            try:
                pkt = await asyncio.wait_for(self.reader.readuntil(b'##'), timeout=1)
            except asyncio.TimeoutError:
                pass
            else:
                # from now on, packets are strings
                msg = pkt.decode('ascii')
                # self.log('packet (%d)=> %s' % (ctr, msg))
                self.log('<= %s' % (msg))
                await self.msg_handler(msg)
                ctr += 1
        self.transport.close()
        self.log('AsyncIOOWNConnection.run : %s the end' % (str(self)))

    def stop(self):
        self.log('stop requested', LOG_DEBUG)
        self._run = False

    async def send_packet(self, msg):
        self.log('=> %s' % (msg))
        if isinstance(msg, str):
            pkt = msg.encode('ascii')
            self.writer.write(pkt)
        await self.writer.drain()

    async def state_start(self, msg):
        if msg == self.ACK:
            self.msg_handler = self.state_login
            cmd_msg = self.SOCKET_MODES[self.mode]
            await self.send_packet(cmd_msg)
        else:
            self.log('we didn\'t get ACK')

    async def state_login(self, msg):
        if msg == '*98*2##':
            # this is a call for sha2 hmac authentication
            self.msg_handler = self.state_hmac_sha2
            await self.send_packet(self.ACK)
        else:
            # attempt matching the old password system
            ops_m = re.match(r'^\*#(\d+)##$', msg)
            if ops_m is not None:
                nonce = ops_m.groups()[0]
                # calculate the password
                passwd = ownCalcPass(self.passwd, nonce)
                passwd_msg = ('*#%s##' % (passwd))
                self.msg_handler = self.state_auth
                await self.send_packet(passwd_msg)
            else:
                self.log("unable to parse the openpassword nonce request")
                await asyncio.sleep(0)

    async def state_hmac_sha2(self, msg):
        ra_m = re.match(r'^\*#(\d{128})##$', msg)
        if ra_m is not None:
            ra = ra_m.group(1)
            hmac = ownCalcHmacSha2(self.passwd, ra)
            rb, hmac_client, self.hmac_server = hmac
            self.msg_handler = self.state_hmac_sha2_check_response
            hmac_packet = ('*#%s*%s##' % (rb, hmac_client))
            await self.send_packet(hmac_packet)
        else:
            self.log("unable to parse the hmac_sha2 request")
            await asyncio.sleep(0)

    async def state_hmac_sha2_check_response(self, msg):
        c_resp_m = re.match(r'^\*#(\d{128})##$', msg)
        if c_resp_m is not None:
                c_resp = c_resp_m.group(1)
                if c_resp == self.hmac_server:
                    self.is_ready.set()
                    self.msg_handler = self.state_dispatch
                    await self.send_packet(self.ACK)
                    
                else:
                    self.log("wrong response from server, expected %s", self.hmac_server)
                    await asyncio.sleep(0)
        else:
            self.log("unable to parse the hmac_sha2 request")
            await asyncio.sleep(0)

    async def state_auth(self, msg):
        if msg == self.ACK:
            self.is_ready.set()
            self.msg_handler = self.state_dispatch

    async def state_dispatch(self, msg):
        await self.queue.put((msg, self.mode, ))
