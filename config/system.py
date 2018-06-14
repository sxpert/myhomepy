# -*- coding: utf-8 -*-

import asyncio

import database
from core.logger import LOG_INFO, LOG_ERROR

from . import callbacks, gateway


class System(object):

    def __init__(self, log=None):
        self.log = log
        self._free = None
        self._task = None
        self.task_queue = asyncio.Queue()
        # things loaded from the configuration
        self.name = None
        self._db = None
        self._database = None
        self.gateway = None
        self.devices = None
        self._callbacks = None
        self.monitor = None
        self.systems = None

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__, self.gateway)

    @property
    def database(self):
        if self._db is None:
            if self._database is None:
                self.log('config.System.database WARNING : '
                         'No database specified anywhere')
            else:
                self.log('config.System.database : '
                         'Opening database %s' % (self._database),
                         LOG_INFO)
                self._db = database.Database(self._database, self)
        return self._db

    @property
    def id(self):
        if not self.systems:
            return None
        return self.systems.index(self)

    @property
    def display_name(self):
        if self.name is None:
            return 'System #%d' % (self.id)
        else:
            return self.name

    @property
    def has_task_queue(self):
        return self.task_queue is not None

    @property
    def async_loop(self):
        if not self.systems:
            self.log("ERROR: Unable to access the systems list object")
            return None
        al = getattr(self.systems, 'async_loop', None)
        if al is None:
            self.log('WARNING: async_loop is None')
        return al

    @property
    def is_cmd_busy(self):
        return not self._free.is_set()

    def set_gateway(self, gateway):
        self.gateway = gateway
        gateway.set_system(self)
        return self

    def loads(self, data):
        if type(data) is not dict:
            self.log("ERROR loading System, dictionnary expected")
        else:
            self.name = data.get('name', None)
            self._database = data.get('database', None)
            self.log('database: %s' % (self._database))
            gateway_data = data.get('gateway', None)
            if gateway_data is not None:
                self.gateway = gateway.Gateway(self)
                self.gateway.loads(gateway_data)
            else:
                self.log("WARNING: no gateway entry in system")
            _devices = data.get('devices', None)
            from myopen.devices import Devices
            self.devices = Devices(self)
            if _devices is not None:
                self.devices.loads(_devices)
            self.log("system.devices %s" % (str(self.devices)))
            callbacks_data = data.get('callbacks', None)
            if callbacks_data is not None:
                self._callbacks = callbacks.Callbacks(self)
                self._callbacks.loads(callbacks_data)
        return self

    def __to_json__(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        data['database'] = self._database
        data['gateway'] = self.gateway
        data['devices'] = self.devices
        data['callbacks'] = self._callbacks
        return data

    async def run_tasks(self):
        self._free = asyncio.Event()
        self._free.set()
        from myopen.commands import BaseCommand
        while self.async_loop.is_running():
            await asyncio.wait([
                self.gateway.is_ready(),
                self._free.wait()])
            
            self._task = await self.task_queue.get()
            self.log('System.run_tasks : task %s' % str(self._task))
            self._free.clear()
            taskcls = self._task.get('task', None)
            if issubclass(taskcls, BaseCommand):
                params = self._task.get('params', None)
                callback = self._task.get('callback', None)
                self._task = taskcls(self, params, callback)
                self._task.start()
            else:
                self.log('System.run_tasks: Invalid task ERROR %s'
                         % (str(self._task)))
                self._task = None

    def dispatch_message(self, msg):
        """
        takes a Message instance, and sends it to the
        current task, if there is one
        """
        if self.is_cmd_busy:
            if msg is not None and self._task is not None:
                dispatch = getattr(self._task, 'dispatch', None)
                if dispatch is None:
                    # should not happen
                    self.log('the %s command has no \'dispatch\' method, can\'t send message %s'
                             % (str(self._task), str(msg)))
                    return False
                if callable(dispatch):
                    res = dispatch(msg)  # pylint: disable=E1102
            else:
                res = None

            if self._task is not None and self._task.is_done:
                self.log('System.dispatch_message : command %s is done' % (str(self._task)))
                self._task = None
                self.gateway.stop_cmd_conn()
                self._free.set()
            return res

    def push_task(self, task, wait=True, callback=None, params=None):
        self.log('push task', LOG_ERROR)
        if self.has_task_queue:
            taskinfo = {
                'task': task,
                'params': params,
                'callback': callback
            }
            self.log('new task %s' % (str(taskinfo)))
            return self.task_queue.put_nowait(taskinfo)
        else:
            self.log('No task queue', LOG_ERROR)

    def run(self):
        """
        initializes the asyncio based coroutines.
        - starts up the gateway with the default monitor connection
        - adds a task list manager
        - if there are no devices registered, posts a scanning task
          to the queue
        """
        self.monitor = self.gateway
        self.gateway.setup_async()
        asyncio.ensure_future(self.run_tasks(), loop=self.async_loop)
        from myopen.commands.asyncio_get_gateway_info import GetGatewayInfo
        self.push_task(GetGatewayInfo)        
        if len(self.devices) == 0:
            from myopen.commands.asyncio_cmd_scan_aid import CmdScanAid
            self.push_task(CmdScanAid)
        return True

    def callback(self, *args, **kwargs):
        if self._callbacks is None:
            self.log('System.callback WARNING : no callbacks found %s %s' % (str(args), str(kwargs)), LOG_INFO)
            return None
        self.log('System.callback : executing callback %s %s' % (str(args), str(kwargs)), LOG_INFO)
        return self._callbacks.execute(*args, **kwargs)

    def socket(self, mode):
        return self.gateway.socket(mode)
