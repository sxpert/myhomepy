# -*- coding: utf-8 -*-

from myopen.subsystems import find_subsystem
import os
import sys
from . import callbacks

PLUGINS_DIRS = "plugins/"


class Condition(object):
    _log = None

    _system_str = None
    _order_str = None
    _device = None

    _subsystem_class = None
    _callback_id = None

    def __init__(self, logger):
        self._log = logger

    def __str__(self):
        return "<%s (%s,%s)=>\'%s\'>" % (
            self.__class__.__name__,
            self._system_str,
            self._order_str,
            self.map_condition()
        )

    def load(self, data):
        self._system_str = data.get("system", None)
        self._order_str = data.get("order", None)
        self._device = data.get("device", None)

        self._subsystem_class = find_subsystem(self._system_str)
        self._callback_id = self._subsystem_class.map_callback_name(self._order_str)
        if self._callback_id is None:
            self._log("Unable to find callback \'%s\'" % (self._order_str))
            return

    def __to_json__(self):
        cn = {}
        cn['system'] = self._system_str
        cn['order'] = self._order_str
        cn['device'] = self._device
        return cn

    @property
    def device(self):
        return self._device

    def map_condition(self):
        return self._subsystem_class().map_callback(self._callback_id, self._device)


class Action(object):
    _log = None

    AC_BUILT_IN = 1 
    AC_PLUGIN = 2

    _action_mode = None

    _module = None
    _method = None

    _params = None

    def __init__(self, logger):
        self._log = logger

    def __str__(self):
        a = 'Unknown'
        if self._action_mode == self.AC_PLUGIN:
            a = "Plugin(%s, %s, %s)" % (
                self._module,
                self._method,
                str(self._params)
            )
        return "<%s %s>" % (
            self.__class__.__name__, a)

    def load(self, data):
        _plugin = data.get("plugin", None)
        if _plugin is not None and isinstance(_plugin, dict):
            self._action_mode = self.AC_PLUGIN
            self._module = _plugin.get("module", None)
            if self._module is None:
                self._log("no module specified for plugin...")
            self._method = _plugin.get("method", None)
            if self._method is None:
                self._log("no method specified for plugin...")
        self._params = data.get("params", None)

    def __to_json__(self):
        ac = {}
        if self._action_mode == self.AC_PLUGIN:
            pl = {}
            pl['module'] = self._module
            pl['method'] = self._method
            ac['plugin'] = pl
        ac['params'] = self._params
        return ac

    def execute(self, system, order, device, data):
        if self._action_mode == self.AC_PLUGIN:
            return self._exec_plugin(system, order, device, data)
        return None
            
    def _exec_plugin(self, subsystem, order, device, data):
        if self._module is None:
            self._log("Module not specified, cancelling callback")
            return None
        if self._method is None:
            self._log("Method not specified, cancelling callback")
            return None
        plugins_paths = PLUGINS_DIRS.split(os.pathsep)
        sys.path.extend(plugins_paths)
        # find the file
        m = None
        for path in plugins_paths:
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                if ext.endswith(".py") and (name == self._module):
                    m = __import__(name, globals())
        if m is None:
            return None
        # find method
        func = getattr(m, self._method, None)
        if func:
            return func(subsystem, self._params, device, data)
        return None


class Callback(object):
    _log = None
    callbacks = None
    condition = None
    action = None

    def __init__(self, obj=None):
        if obj is not None:
            if isinstance(obj, callbacks.Callbacks):
                self.callbacks = obj
                self._log = self.callbacks.log
            else:
                self.log("WARNING: wrong object passed "
                         "to Callback.__init__ %s" % (str(obj)))

    def log(self, msg):
        if self._log is not None:
            self._log(msg)
        else:
            print(msg)

    def __str__(self):
        return "<%s %s %s>" % (
            self.__class__.__name__,
            str(self.condition),
            str(self.action)
        )

    def load(self, data):
        # callbacks must have 2 sections :
        cond_data = data.get("conditions", None)
        if cond_data is None:
            cond_data = data.get("condition", None)
        if cond_data is not None:
            self.condition = Condition(self._log)
            self.condition.load(cond_data)
        action_data = data.get("action", None)
        if action_data is not None:
            self.action = Action(self._log)
            self.action.load(action_data)
        self.log(str(self))

    def __to_json__(self):
        data = {}
        if self.condition:
            data['condition'] = self.condition
        if self.action:
            data['action'] = self.action
        else:
            self.log('action is None...')
        self.log(data)
        return data

    def map_callback(self):
        return self.condition.map_condition()

    def execute(self, subsystem, order, device, data):
        if self.action is not None:
            return self.action.execute(subsystem, order, device, data)
        self.log("self.action is None => return None")
        return None
