# -*- coding: utf-8 -*-

from .basedevice import BaseDevice

class Devices(object):
    _devs = {}

    def __init__(self, system):
        self._system = system
        self._discovery_busy = False
        self._active_device = None

    def log(self, msg):
        self._system.log(msg)
    
    def load(self, data):
        pass

    def __to_json__(self):
        if len(self._devs) == 0:
            return None
        # make a list of devices
        data = []
        for k in self._devs.keys():
            data.append(self._devs[k])
        return data

    # dict interface

    def keys(self):
        return self._devs.keys()

    def __len__(self):
        return len(self._devs)

    def __getitem__(self, key):
        return self._devs[key]

    def __setitem__(self, key, item):
        self._devs[key] = item

    # def __str__(self):
    #     _s = '<%s>' % (self.__class__.__name__)
    #     return _s
    
    @staticmethod
    def format_hw_addr(hw_addr):
        return '%08X' % (hw_addr)

    def register(self, subsystem, data):
        # build proxy device
        d = BaseDevice(subsystem, data)
        if not d.valid:
            self.log('ERROR: malformed device register request, missing \'hw_addr\' value %s %s' %
                (str(subsystem), str(data)))        
            return None
        k = Devices.format_hw_addr(d.hw_addr)
        # if device already registered, return that
        if k in self.keys():
            return self[k]
        # insert proxy device
        self[k] = d
        # push command to get device info
        self.log('Device %s is not yet known, queuing for discovery' % (k))
        from ..commands import CmdDiagDeviceByAid
        self._system.monitor.push_task(CmdDiagDeviceByAid, 
                                    params={'devices': self,
                                            'device': d })    
        return d

    def set_active_device(self, caller, hw_addr):
        self.log('set_active_device %s %s' % (str(caller), str(hw_addr)))
        if self._active_device is not None:
            self.log('active device already set to %s' % (self._active_device))
            return True
        k = self.format_hw_addr(hw_addr)
        if k in self.keys():
            self._active_device = self[k]
            self._active_device_caller = caller
            return True
        self.log('unable to find device with hw_addr %s' % (k))
        return False

    def reset_active_device(self):
        self.log('resetting active device')
        self._active_device = None
        self._active_device_caller = None

    def eot_event(self, command, matches):
        self.log('Devices.eot_event')
        from ..dialog import CommandDialog
        self.log('%s' % (self._active_device_caller))
        if issubclass(self._active_device_caller.__class__, CommandDialog):
            self.log('we have a CommandDialog subclass object')
            if self._active_device is not None:
                self.log('notifying diag sync')
                return self._active_device_caller.notify_diag_sync()
        return False


