# -*- coding: utf-8 -*-

from .basedevice import BaseDevice
from core.logger import LOG_ERROR, LOG_INFO, LOG_DEBUG
from myopen.subsystems import find_subsystem


class Devices(object):

    def __init__(self, system):
        self._devs = {}
        self.system = system
        self.log = system.log
        self._discovery_busy = False
        self._active_device = None

    def loads(self, data):
        if not isinstance(data, list):
            self.log('Devices.loads : devices should contain a list',
                     LOG_ERROR)
            return None
        # we have a list
        for dev_data in data:
            subsystem = dev_data.get('subsystem', None)
            subs = find_subsystem(subsystem)
            # at this point, hw_addr is an 8 chars hex string
            hw_addr = dev_data.get('hw_addr', None)
            if hw_addr is not None and len(hw_addr) == 8:
                hw_addr = int(hw_addr, 16)
                dev_data['hw_addr'] = hw_addr
            dev = BaseDevice(self, subs, dev_data)
            dev = dev.loads(dev_data)
            # add device to list
            k = Devices.format_hw_addr(dev.hw_addr)
            self._devs[k] = dev
            # if device is BaseDevice...
            self.log('Devices.loads : device class %s'
                     % (str(dev.__class__)), LOG_DEBUG)
            self.log('Devices.loads : device is BaseDevice ? %s'
                     % (str(dev.__class__ is BaseDevice)), LOG_DEBUG)
            if dev.__class__ is BaseDevice:
                self.log('Devices.loads : queuing %s' % (str(dev)),
                         LOG_ERROR)
                dev.queue_for_discovery()

    def __to_json__(self):
        if len(self._devs) == 0:
            return None
        # make a list of devices
        data = []
        for k in sorted(self._devs.keys()):
            data.append(self._devs[k])
        return data

    # dict interface

    def keys(self):
        return self._devs.keys()

    def __len__(self):
        l = len(self._devs)
        self.log('requested length %d returned' % l, LOG_ERROR)
        return l

    def __getitem__(self, key):
        self.log('requested item with key %s %s' % (str(type(key)), str(key)), LOG_ERROR)
        if isinstance(key, int):
            keys = sorted(self._devs.keys())
            self.log(keys, LOG_ERROR)
            if key in range(0, len(keys)):
                return self._devs[keys[key]]
            raise KeyError
        return self._devs[key]

    def __iter__(self):
        return self._devs.__iter__()
    
    def items(self):
        return self._devs.items()
                
    def __setitem__(self, key, item):
        self._devs[key] = item

    # def __str__(self):
    #     _s = '<%s>' % (self.__class__.__name__)
    #     return _s

    @staticmethod
    def format_hw_addr(hw_addr):
        if not isinstance(hw_addr, int):
            hw_addr = int(hw_addr)
        return '%08X' % (hw_addr)

    def _register(self, subsystem, data):
        """
        Registers a device without launching a scan
        """

        hw_addr = data.get('hw_addr', None)
        if hw_addr is None:
            self.log('ERROR: malformed device register request, '
                     'missing \'hw_addr\' value %s %s' %
                     (str(subsystem), str(data)))
            return None
        # generate key
        k = Devices.format_hw_addr(hw_addr)
        # if device already registered, return that
        if k in self.keys():
            dev = self[k]
            dev.update_base_data(data)
            return dev
        # build proxy device
        d = BaseDevice(self, subsystem, data)
        # should not happen
        if not d.valid:
            self.log('ERROR: proxy device is not valid')
            return None
        # insert proxy device
        self[k] = d
        return d

    def register(self, subsystem, data):
        """
        Registers a device, launches a scan if the device is unknown
        """
        dev = self._register(subsystem, data)
        self.log('Devices.register : %s' % (str(dev)), LOG_INFO)
        if dev.__class__.__name__ != BaseDevice.__name__:
            return dev
        # push command to get device info
        dev.queue_for_discovery()
        return dev

    def set_active_device(self, caller, hw_addr):
        if self._active_device is not None:
            self.log('active device already set to %s' %
                     (self._active_device), LOG_INFO)
            return True
        k = self.format_hw_addr(hw_addr)
        if k not in self.keys():
            # registers the device
            self._register(caller, {'hw_addr': hw_addr})
        self.log('setting active device to %s' % (str(self[k])), LOG_ERROR)
        self._active_device = self[k]
        self._active_device_caller = caller
        return True

    def replace_active_device(self, new_device):
        if self._active_device is None:
            self.log('Devices.replace_active_device: no device activated')
            return False

        bd_name = BaseDevice.__name__
        ad_name = self._active_device.__class__.__name__
        nd_name = new_device.__class__.__name__

        if ad_name != bd_name:
            self.log('Devices.replace_active_device: '
                     'active device not an instance of BaseDevice',
                     LOG_INFO)
            return False

        if nd_name == bd_name:
            self.log('Devices.replace_active_device: '
                     'new device should not be an instance of BaseDevice',
                     LOG_INFO)
            return False

        old_hw_addr = self._active_device.hw_addr
        new_hw_addr = new_device.hw_addr
        old_x = self.format_hw_addr(old_hw_addr)
        new_x = self.format_hw_addr(new_hw_addr)
        if old_hw_addr != new_hw_addr:
            self.log('Devices.replace_active_device: '
                     'hardware addresses must match %s => %s' % (old_x, new_x),
                     LOG_INFO)
            return False

        # we are reasonably certain of having the right things here
        self[new_x] = new_device
        self._active_device = new_device

        return True

    def res_object_model(self, virt_id, model_id,
                         nb_conf, brand_id, prod_line):
        if self._active_device is not None:
            return self._active_device\
                .res_object_model(virt_id, model_id,
                                  nb_conf, brand_id, prod_line)
        self.log('Devices.res_object_model : no active device', LOG_INFO)
        return False

    def res_fw_version(self, virt_id, fw_version):
        if self._active_device is not None:
            return self._active_device.res_fw_version(virt_id, fw_version)
        self.log('Devices.res_fw_version : no active device', LOG_INFO)
        return False

    def res_conf_1_6(self, virt_id, conf_1_6):
        if self._active_device is not None:
            return self._active_device.res_conf_1_6(virt_id, conf_1_6)
        self.log('Devices.res_conf_1_6 : no active device', LOG_INFO)
        return False

    def res_ko_value(self, virt_id, slot, keyo, state):
        if self._active_device is not None:
            return self._active_device.res_ko_value(virt_id, slot, keyo, state)
        self.log('Devices.res_ko_value : no active device', LOG_INFO)
        return False

    def res_ko_sys(self, virt_id, slot, sys, addr):
        if self._active_device is not None:
            return self._active_device.res_ko_sys(virt_id, slot, sys, addr)
        self.log('Devices.res_ko_sys : no active device', LOG_INFO)
        return False

    def eot_event(self, command, matches):
        # if we have an active device, just reply true
        if self._active_device is not None:
            return True
        # no active device, reply false
        self.log('Devices.eot_event : no active device', LOG_INFO)
        return False

    def res_param_ko(self, virt_id, slot, index, val_par):
        if self._active_device is not None:
            return self._active_device.res_param_ko(virt_id, slot,
                                                    index, val_par)
        self.log('Devices.res_param_ko : no active device', LOG_INFO)
        return False

    def end_config_read(self):
        if self._active_device is not None:
            self._active_device.end_config_read()
        # save configuration
        self.system.systems.config.save()

    def reset_active_device(self):
        if self._active_device is not None:
            # self.log('resetting active device')
            self._active_device = None
            self._active_device_caller = None
            return
        self.log('there was no active device')
