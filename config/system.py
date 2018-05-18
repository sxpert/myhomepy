# -*- coding: utf-8 -*-

import asyncio

import database
from core.logger import *

from . import callbacks, gateway


class System(object):
    _db = None
    _database = None
    gateway = None
    devices = None
    _callbacks = None
    # system = None
    monitor = None
    systems = None

    def __init__(self, log=None):
        self.log = log
        self._free = None
        self._task = None

    def load(self, data):
        if type(data) is not dict:
            self.log("ERROR loading System, dictionnary expected")
        else:
            self._database = data.get('database', None)
            self.log('database: %s' % (self._database))
            gateway_data = data.get('gateway', None)
            if gateway_data is not None:
                self.gateway = gateway.Gateway(self)
                self.gateway.load(gateway_data)
            else:
                self.log("WARNING: no gateway entry in system")
            _devices = data.get('devices', None)
            from myopen.devices import Devices
            self.devices = Devices(self)
            if _devices is not None:
                self.devices.load(_devices)
            self.log("system.devices %s" % (str(self.devices)))
            callbacks_data = data.get('callbacks', None)
            if callbacks_data is not None:
                self._callbacks = callbacks.Callbacks(self)
                self._callbacks.load(callbacks_data)
        return self

    def __to_json__(self):
        data = {}
        data['database'] = self._database
        data['gateway'] = self.gateway
        data['devices'] = self.devices
        data['callbacks'] = self._callbacks
        return data

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
    def main_loop(self):
        if not self.systems:
            self.log("ERROR: Unable to access the systems list object")
            return None
        ml = getattr(self.systems, 'main_loop', None)
        return ml

    @property
    def async_loop(self):
        if not self.systems:
            self.log("ERROR: Unable to access the systems list object")
            return None
        al = getattr(self.systems, 'async_loop', None)
        if al is None:
            self.log('WARNING: async_loop is None')
        return al

    def set_gateway(self, gateway):
        self.gateway = gateway
        gateway.set_system(self)
        return self

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__, self.gateway)

    @property
    def is_cmd_busy(self):
        return not self._free.is_set()

    async def run_tasks(self):
        self._free = asyncio.Event()
        self._free.set()
        from myopen.commands import BaseCommand
        while self.async_loop.is_running():
            await asyncio.wait([
                self.gateway.is_ready(),
                self._free.wait()])
            self._task = await self.task_queue.get()
            self._free.clear()
            taskcls = self._task.get('task', None)
            if issubclass(taskcls, BaseCommand):
                params = self._task.get('params', None)
                self._task = taskcls(self, params)
                self._task.start()
            else:
                self.log('System.run_tasks: Invalid task ERROR %s'
                         % (str(self._task)))
                self._task = None

    def dispatch_message(self, msg):
        if self.is_cmd_busy:
            if msg is not None and self._task is not None:
                dispatch = getattr(self._task, 'dispatch', None)
                if dispatch is None:
                    # should not happen
                    self.log('the %s command has no \'dispatch\' method, '
                             'can\'t send message %s'
                             % (str(self._task), str(msg)))
                    return False
                res = dispatch(msg)
            else:
                res = None

            if self._task is not None and self._task.is_done:
                self.log('System.dispatch_message : command %s is done'
                         % (str(self._task)))
                self._task = None
                self.gateway.stop_cmd_conn()
                self._free.set()

            return res

    def push_task(self, task, wait=True, callback=None, params=None):
        if self.async_loop is not None:
            taskinfo = {
                'task': task,
                'params': params
            }
            self.log('new task %s' % (str(taskinfo)))
            return self.task_queue.put_nowait(taskinfo)
        if self.main_loop:
            return self.monitor.push_task(task, wait, callback, params)

    def run_async(self):
        """
        initializes the asyncio based coroutines.
        - starts up the gateway with the default monitor connection
        - adds a task list manager
        - if there are no devices registered, posts a scanning task
          to the queue
        """
        import asyncio
        self.monitor = self.gateway
        self.gateway.setup_async()
        self.task_queue = asyncio.Queue(loop=self.async_loop)
        asyncio.ensure_future(self.run_tasks(), loop=self.async_loop)
        if len(self.devices) == 0:
            from myopen.commands.asyncio_cmd_scan_aid import CmdScanAid
            self.push_task(CmdScanAid)

    def run(self):
        # try main_loop (thread based)
        if self.main_loop is not None:
            from myopen.monitor import OWNMonitor
            self.monitor = OWNMonitor(self)
            return True
        if self.async_loop is not None:
            self.run_async()
            return True
        self.log("ERROR: Unable to start system, there is no system loop")
        return False

    def callback(self, *args, **kwargs):
        if self._callbacks is None:
            self.log('System.callback WARNING : '
                     'no callbacks found %s %s' % (str(args), str(kwargs)),
                     LOG_INFO)
            return None
        self.log('System.callback : executing callback %s %s' %
                 (str(args), str(kwargs)),
                 LOG_INFO)
        return self._callbacks.execute(*args, **kwargs)

    def socket(self, mode):
        return self.gateway.socket(mode)
