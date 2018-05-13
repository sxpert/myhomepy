# -*- coding: utf-8 -*-

import json

class BaseDevice(json.JSONEncoder):
    BRAND_UNDEFINED = 0
    BRAND_BTICINO = 1
    BRAND_LEGRAND = 2
    BRAND_TEGUI = 3
    BRAND_KONTAKTOR = 4
    BRAND_SHIDEAN = 5
    BRAND_OBSOLETE_1 = 6
    BRAND_LEGRAND_GROUP = 7
    BRAND_LEGRAND_BTICINO = 8
    BRAND_ARNOULD = 9

    BRANDS_SHORT_NAME = 0
    BRANDS_LONG_NAME = 1
    BRANDS = (
        ('_', 'UNDEFINED', ),
        ('BT', 'BTicino', ),
        ('LG', 'Legrand', ),
        ('TG', 'Tegui', ),
        ('KT', 'Kontaktor', ),
        ('SH', 'Shidean', ),
        ('_0', 'OBSOLETE', ),
        ('LGG', 'LegrandGroup', ),
        ('LGG', 'LegrandBticino', ),
        ('AR', 'Arnould', ),
    )

    PROD_LINE_UNDEFINED = 0
    PROD_LINE_CELIANE = 4

    PROD_LINES = (
        'UNDEFINED', 
        None,
        None,
        None,
        'Céliane', 
    )

    PARAMS_KEY = '_PARAMS'

    def __init__(self, devices, subsystem, params):
        self._devices = devices
        self._subsystem = subsystem
        self._virt_id = params.get('virt_id', None)
        self._hw_addr = params.get('hw_addr', None)
        if isinstance(self._hw_addr, str):
            # TODO: check if we get an exception
            self._hw_addr = int(self._hw_addr)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        _class = '<%s ' % (self.__class__.__name__)
        if self.valid:
            from . import Devices
            return '%sid: %s>' % (_class, Devices.format_hw_addr(self._hw_addr))
        return '%sINVALID>' % (_class)

    def dump_configurators(self):
        """
        dumps device configurators in a human readable version,
        suitable for use in the configuration save, for instance

        returns None if no configurators are present
        can return either an array, or a dictionnary, depending on 
        the device
        """
        confs = getattr(self, '_configurators', None)
        if confs is None:
            return None
        return confs

    def dump_brand(self):
        bid = getattr(self, '_brand_id', None)
        if bid is None:
            return bid
        if not isinstance(bid, int):
            return bid
        if bid < 0 or bid >= len(self.BRANDS):
            return bid
        return self.BRANDS[bid][self.BRANDS_LONG_NAME]

    def dump_product_line(self):
        pln = getattr(self, '_product_line', None)
        if pln is None:
            return pln
        if not isinstance(pln, int):
            return pln
        if pln <0 or pln >= len(self.PROD_LINES):
            return pln
        pln_s = self.PROD_LINES[pln]
        if pln_s is None:
            return pln
        return pln_s

    def dump_slots(self):
        slots = getattr(self, '_slots', None)
        return slots

    def __to_json__(self):
        data = {}
        data['virt_id'] = self._virt_id
        data['hw_addr'] = self._hw_addr

        # MODEL_ID handling
        # the proper model_id
        model_id = getattr(self, 'MODEL_ID', None)
        if model_id is not None:
            data['model_id'] = model_id
        # if the model wasn't known, this may be available
        if model_id is None:
            model_id = getattr(self, '_model_id', None)
            if model_id is not None:
                data['_model_id'] = model_id

        confs = self.dump_configurators()
        if confs is not None:
            data['configurators'] = confs

        brand_id = self.dump_brand()
        if brand_id is not None:
            data['brand_id'] = brand_id

        prod_line = self.dump_product_line()
        if prod_line is not None:
            data['product_line'] = prod_line

        fw_version = getattr(self, '_fw_version', None)
        if fw_version is not None:
            data['firmware_version'] = fw_version

        slots = self.dump_slots()
        if slots is not None:
            data['slots'] = slots

        return data

    @property
    def valid(self):
        return self._subsystem is not None and \
               self._virt_id is not None and \
               self._hw_addr is not None

    @property
    def hw_addr(self):
        return self._hw_addr

    def res_object_model(self, virt_id, model_id, nb_conf, brand_id, prod_line):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            # self._devices.log('we are an instance of BaseDevice, time to setup the proper type')
            from . import DeviceTypes
            for d in DeviceTypes:
                mid = getattr(d, 'MODEL_ID', None) 
                if mid is not None and mid == model_id:
                    nd = d(self._devices, self._subsystem, {'virt_id': self._virt_id, 'hw_addr': self._hw_addr})
                    nd.res_object_model(virt_id, model_id, nb_conf, brand_id, prod_line)
                    self._devices.replace_active_device(nd)
                    return True
            # couldn't find a proper model id
            self._model_id = model_id
            return False
        # self._devices.log('we are an instance of %s' % (self.__class__.__name__))
        self._configurators = [0] * nb_conf
        self._brand_id = brand_id
        self._product_line = prod_line
        return True

    def res_fw_version(self, virt_id, fw_version):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self._devices.log('can\'t set the firmware version on a BaseDevice instance')
            return False
        self._fw_version = fw_version
        return True

    def set_configurator(self, index, value):
        if not hasattr(self, '_configurators'):
            return False
        if index < 0 or index >= len(self._configurators):
            return False
        self._configurators[index] = value
        return True

    def res_conf_1_6(self, virt_id, conf_1_6):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self._devices.log('can\'t set configurators 1 through 6 on a BaseDevice instance')
            return False
        # limit the range to the actual number of configurators
        range_max = min(len(self._configurators), 6)
        for i in range(0, range_max):
            v = conf_1_6[i]
            if not self.set_configurator(i, v):
                self._devices.log('Unable to set configurator %d to value %d' % (i, v))
        return True

    def _slots_check(self, slot_id):
        slots = getattr(self, '_slots', [])
        # slot ids start at 1
        if slot_id < 1:
            self._devices.log('slot_set_value : slot_id %d invalid' % (slot_id))
        if slot_id > 32:
            self._devices.log('slot_set_value : slot_id %d appears too large' % (slot_id))
        if len(slots) < slot_id:
            # enlarge (hihi) the slots
            slots += [None]*(slot_id-len(slots))
            self._slots = slots
        return slots

    def slot_get_slot(self, slot_id):
        slots = self._slots_check(slot_id)
        # slot_id starts at 1
        return slots[slot_id-1]

    def slot_set_slot(self, slot_id, slot_contents):
        slots = self._slots_check(slot_id)
        # slot_id starts at 1
        slots[slot_id-1] = slot_contents
        return True

    def slot_get_value(self, slot_id, key, default=None):
        slot = self.slot_get_slot(slot_id)
        if slot is None:
            return default
        return slot.get(key, default)

    def slot_set_value(self, slot_id, key, value):
        slot = self.slot_get_slot(slot_id)
        if slot is None:
            slot = {}
        slot[key] = value
        self.slot_set_slot(slot_id, slot)

    def slot_set_param(self, slot_id, index, val_par):
        params = self.slot_get_value(slot_id, self.PARAMS_KEY, {})
        params[index] = val_par
        self.slot_set_value(slot_id, self.PARAMS_KEY, params)

    def res_ko_value(self, virt_id, slot, keyo, state):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self._devices.log('can\'t set keyo and state on a BaseDevice instance')
            return False
        self.slot_set_value(slot, 'keyo', keyo)
        self.slot_set_value(slot, 'state', state)
        return True

    def res_ko_sys(self, virt_id, slot, sys, addr):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self._devices.log('can\'t set sys and addr on a BaseDevice instance')
            return False
        self.slot_set_value(slot, 'sys', sys)
        self.slot_set_value(slot, 'addr', addr)
        return True

    def res_param_ko(self, virt_id, slot, index, val_par):
        if virt_id != self._virt_id:
            self._devices.log('this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id))
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self._devices.log('can\'t set parameter on a BaseDevice instance')
            return False
        self.slot_set_param(slot, index, val_par)
        return True

    def end_config_read(self):
        return