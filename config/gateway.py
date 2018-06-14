# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, timedelta

from core.logger import LOG_INFO, COLOR_LT_RED, get_logger
from myopen.asyncio_connection import AsyncIOOWNConnection, MODE_COMMAND, MODE_MONITOR
from myopen.message import Message

from . import system


class Gateway(object):
    address = None
    port = None
    passwd = None
    available = False
    system = None
    proxy_port = None
    proxy = None

    _cur_date = None
    _cur_time = None

    def __init__(self, *args, **kwargs):
        self.log = None
        if len(args) == 1:
            obj = args[0]
            if isinstance(obj, system.System):
                self.system = obj
                self.log = obj.log
        elif len(args) == 3:
            if isinstance(args[0], str) and \
               isinstance(args[1], int) and \
               isinstance(args[2], str):
                self.address = args[0]
                self.port = args[1]
                self.passwd = args[2]
                self.available = True
        if self.log is None:
            self.log = get_logger(LOG_INFO, color=COLOR_LT_RED)
        self.log("Invalid parameters on creating Gateway")
        self.log(args)
        self.log(kwargs)

    def set_system(self, system):
        self.system = system
        self.log = system.log

    @property
    def display_name(self):
        name = getattr(self, '_name', None)
        if name is None:
            return self.address
        return name

    @property
    def model(self):
        model = getattr(self, '_model', None)
        if model is None:
            return "F454"
        return model

    def loads(self, data):
        if type(data) is not dict:
            self.log("ERROR loading Gateway, dictionnary expected")
        else:
            self.address = data.get('ip', None)
            if not self.address:
                self.address = data.get('address', None)
            if not self.address:
                self.log("WARNING: no address specified for this system's gateway")
            self.port = data.get('port', None)
            if not self.port:
                self.log("WARNING: no port specified for this system's gateway, using default 20000")
                self.port = 20000
            self.passwd = data.get('password', None)
            if not self.passwd:
                self.passwd = data.get('passwd', None)
            if not self.passwd:
                self.log("WARNING: no open password specified for this system's gateway")
            self.set_available()
            if not self.available:
                self.log("WARNING: problems in gateway configuration, this system will not be available")
            else:
                self.log("Gateway %s ready" % str(self))
            self.proxy_port = data.get('proxy_port', None)
        return self

    def __to_json__(self):
        data = {}
        data['address'] = self.address
        data['port'] = self.port
        data['passwd'] = self.passwd
        if self.proxy_port is not None:
            data['proxy_port'] = self.proxy_port
        return data

    def set_available(self):
        if self.address and self.port and self.passwd:
            self.available = True
        else:
            self.available = False

    def __repr__(self):
        address_s = str(self.address)
        port_s = str(self.port)
        # don't show password in logs
        passwd_s = '**********'
        return '<%s address: %s port: %s passwd: \'%s\'>' % (self.__class__.__name__, address_s, port_s, passwd_s)

    # ------------------------------------------------------------------------
    #
    # socket related stuff
    #

    @property
    def socket_info(self):
        return (self.address, self.port, self.passwd, )

    async def is_ready(self):
        await self.mon_conn.is_ready.wait()

    def send(self, msg):
        self.send_queue.put_nowait(msg)

    async def handle_send_queue(self):
        while self.loop.is_running():
            pkt = await self.send_queue.get()
            if self.cmd_conn is None:
                self.log('Gateway.handle_send_queue : starting the command connection')
                self.cmd_conn = \
                    AsyncIOOWNConnection(self.address,
                                         self.port,
                                         self.passwd,
                                         self.msg_queue,
                                         MODE_COMMAND,
                                         loop=self.loop)
                self.cmd_conn.auto_restart = False
                self.cmd_conn_future = asyncio.ensure_future(self.cmd_conn.run(), loop=self.loop)
                await self.cmd_conn.is_ready.wait()
                self.log('Gateway.handle_send_queue : CMD conn is ready')
            self.log('Gateway.handle_send_queue : sending \'%s\'' % (str(pkt)))
            await self.cmd_conn.send_packet(pkt)

    def stop_cmd_conn(self):
        self.log('end of the command connection')
        if self.cmd_conn is not None:
            self.cmd_conn.stop()
            if self.cmd_conn_future is not None:
                asyncio.wait(self.cmd_conn_future)
                self.cmd_conn_future = None
            self.cmd_conn = None

    def setup_async(self):
        self.loop = self.system.async_loop
        self.loop = asyncio.get_event_loop()
        self.send_queue = asyncio.Queue(loop=self.loop)
        self.msg_queue = asyncio.Queue(loop=self.loop)
        asyncio.ensure_future(self.run(), loop=self.loop)
        asyncio.ensure_future(self.handle_send_queue(), loop=self.loop)
        self.mon_conn = \
            AsyncIOOWNConnection(self.address,
                                 self.port,
                                 self.passwd,
                                 self.msg_queue,
                                 MODE_MONITOR,
                                 loop=self.loop)
        self.cmd_conn = None
        self.cmd_conn_task = None
        asyncio.ensure_future(self.mon_conn.run(), loop=self.loop)

        # transparent proxy
        if self.proxy_port is not None:
            self.proxy = None

    async def run(self):
        while True:
            try:
                data = await asyncio.wait_for(self.msg_queue.get(), .2)
            except asyncio.TimeoutError:
                data = None

            if data is not None:
                # send the message to websocket listener
                try:
                    await self.system.websocket_dispatch(data)
                except:
                    import traceback
                    traceback.print_exc()
                handled = False
                if self.system.is_cmd_busy:
                    try:
                        handled = self.system.dispatch_message(data)
                    except:
                        import traceback
                        traceback.print_exc()
                if not handled:
                    try:
                        m = Message(data, self)
                        m.dispatch()
                    except:
                        import traceback
                        traceback.print_exc()

    # ------------------------------------------------------------------------
    #
    # gateway specific functions
    #

    # gateway sends date then time every 10 minutes...

    def _check_and_update_date_time(self):
        if self._cur_date is not None and self._cur_time is not None:
            _g_dt = datetime.combine(self._cur_date, self._cur_time)
            _sys_dt = datetime.now().astimezone()
            _offset = _sys_dt - _g_dt
            self.log('system %s gateway %s offset %s' %
                     (str(_sys_dt), str(_g_dt), str(_offset)),
                     LOG_INFO)
            if abs(_offset) > timedelta(minutes=5):
                self.log('offset too large, queue a gateway datetime '
                         'update to current value',
                         LOG_INFO)
                from myopen.commands import CmdGatewayUpdateDateTime
                params = {
                    'gateway': self,
                    'datetime': _sys_dt
                }
                self.system.push_task(CmdGatewayUpdateDateTime, params=params)

    def date_info(self, _date):
        self._cur_date = _date
        self.log(self._cur_date, LOG_INFO)
        return True

    def time_info(self, _time):
        self._cur_time = _time
        self.log(self._cur_time, LOG_INFO)
        self._check_and_update_date_time()
        return True
