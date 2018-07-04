# -*- coding: utf-8 -*-

from .device import Device
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
        if len(data) == 0:
            self.log("Devices.loads : no devices, push discovery", LOG_ERROR)
            return None
        # we have a list
        for dev_data in data:
            # subsystem = dev_data.get('subsystem', None)
            # subs = find_subsystem(subsystem)
            # # at this point, hw_addr is an 8 chars hex string
            # hw_addr = dev_data.get('hw_addr', None)
            # if hw_addr is not None and len(hw_addr) == 8:
            #     hw_addr = int(hw_addr, 16)
            #     dev_data['hw_addr'] = hw_addr
            
            # dev = Device(self, subs, dev_data)
            dev = Device(self)
            self.log("Devices.loads : %s" % (dev_data))
            dev = dev.loads(dev_data)
            self.log("Devices.loads : %s" % (str(dev)))
            # add device to list
            self._devs[dev.hw_addr_hex] = dev
            # if dev.__class__ is Device:
            #     self.log('Devices.loads : queuing %s' % (str(dev)),
            #              LOG_ERROR)
            #     dev.queue_for_discovery()
        

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
        # create device
        d = Device(self)
        d.subsystem = subsystem
        d.hw_addr = int(hw_addr)
        self.log('Devices._register: adding device %s %s ' % (d.hw_addr_hex, str(d)), LOG_ERROR)
        self[d.hw_addr_hex] = d
        return d

    def register(self, subsystem, data):
        """
        Registers a device, launches a scan if the device is unknown
        """
        self.log("Register device %s %s" % (str(subsystem), str(data)), LOG_ERROR)
        dev = self._register(subsystem, data)
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

        bd_name = Device.__name__
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

    # ------------------------------------------------------------------------
    #
    # config-reactor functions
    #
    #

    def cmd_conf_end(self):
        if self._active_device is not None:
            try:
                self._active_device.cmd_conf_end()
            except Exception:
                pass
            self.system.devices.end_config_read()
            self.system.devices.reset_active_device()
            return True           
        self.log('Devices.cmd_conf_end : no active device', LOG_INFO)
        return False

    def res_trans_end(self):
        # if we have an active device, just reply true
        if self._active_device is not None:
            # nothing to do here, wait for more info...
            return True
        # no active device, reply false
        self.log('Devices.res_trans_end : no active device', LOG_INFO)
        return False

    def cmd_diag_abort(self):
        if self._active_device is not None:
            self.system.devices.end_config_read()
            self.system.devices.reset_active_device()
            return True           
        self.log('Devices.cmd_diag_abort : no active device', LOG_INFO)
        return False

    def cmd_conf_id(self, hw_addr, caller=None):
        return self.set_active_device(caller, hw_addr)

    def cmd_diag_id(self, hw_addr, caller=None):
        return self.set_active_device(caller, hw_addr)

    def cmd_reset_ko(self, slot):
        if self._active_device is not None:
            return self._active_device.cmd_reset_ko(slot)
        self.log('Devices.cmd_reset_ko : no active device', LOG_INFO)
        return False

    def res_conf_ok(self): 
        if self._active_device is not None:
            return self._active_device.res_conf_ok()
        self.log('Devices.res_conf_ok : no active device', LOG_INFO)
        return False

    def res_object_model(self, virt_id, model_id, nb_conf, brand_id, prod_line):
        if self._active_device is not None:
            return self._active_device.res_object_model(virt_id, model_id,nb_conf, brand_id, prod_line)
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

    def res_conf_7_12(self, virt_id, conf_7_12):
        if self._active_device is not None:
            return self._active_device.res_conf_7_12(virt_id, conf_7_12)
        self.log('Devices.res_conf_7_12 : no active device', LOG_INFO)
        return False

    # missing: 
    # res_diag_a
    # res_diag_b
    # res_id (register)

    def res_ko_value(self, virt_id, slot, keyo, state):
        if self._active_device is not None:
            return self._active_device.res_ko_value(virt_id, slot, keyo, state)
        self.log('Devices.res_ko_value : no active device', LOG_INFO)
        return False

    def cmd_ko_value(self, slot, keyo):
        if self._active_device is not None:
            return self._active_device.cmd_ko_value(slot, keyo)
        self.log('Devices.cmd_ko_value : no active device', LOG_INFO)
        return False

    def res_ko_sys(self, virt_id, slot, sys, addr):
        if self._active_device is not None:
            return self._active_device.res_ko_sys(virt_id, slot, sys, addr)
        self.log('Devices.res_ko_sys : no active device', LOG_INFO)
        return False

    def cmd_ko_sys(self, slot, sys, addr):
        if self._active_device is not None:
            return self._active_device.cmd_ko_sys(slot, sys, addr)
        self.log('Devices.cmd_ko_sys : no active device', LOG_INFO)
        return False

    def res_param_ko(self, virt_id, slot, index, val_par):
        if self._active_device is not None:
            return self._active_device.res_param_ko(virt_id, slot, index, val_par)
        self.log('Devices.res_param_ko : no active device', LOG_INFO)
        return False

    def cmd_param_ko(self, slot, index, value):
        if self._active_device is not None:
            return self._active_device.cmd_param_ko(slot, index, value)
        self.log('Devices.cmd_param_ko : no active device', LOG_INFO)
        return False
