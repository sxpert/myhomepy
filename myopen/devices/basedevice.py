# -*- coding: utf-8 -*-

import json, threading

class BaseDevice(json.JSONEncoder):
    # this comes from the MHCatalogue.db file

    BRAND_UNDEFINED = 0
    BRAND_BTICINO = 1
    BRAND_LEGRAND = 2
    BRAND_TEGUI = 3
    BRAND_SHIDEAN = 4
    BRAND_LEGRAND_BTICINO = 5
    BRAND_ARNOULD = 6

    PROD_LINE_UNDEFINED = 0
    PROD_LINE_L_N_NT = 1
    PROD_LINE_VELA = 1
    PROD_LINE_ARTEOR = 2
    PROD_LINE_MATIX = 2
    PROD_LINE_AXOLUTE = 3
    PROD_LINE_MOSAIC = 3
    PROD_LINE_CELIANE = 4
    PROD_LINE_POLYX = 4
    PROD_LINE_GALEA = 5
    PROD_LINE_PIVOT = 6
    PROD_LINE_SFERA = 7
    PROD_LINE_ESPACE_EVOLUTON = 8
    PROD_LINE_ETERIS = 9
    PROD_LINE_AIR = 10

    BRANDS = [
        {   
            'id': 'BRAND_UNDEFINED',
            'names': {
                'short': '_', 
                'long': 'Undefined'
            },
            'lines': {
                PROD_LINE_UNDEFINED: 'Undefined'
            }
        },
        {   
            'id': 'BRAND_BTICINO',
            'names': {
                'short': 'BT',
                'long': 'BTicino'
            },
            'lines': {
                PROD_LINE_L_N_NT: 'L/N/NT',
                PROD_LINE_MATIX: 'Matix',
                PROD_LINE_AXOLUTE: 'Axolute',
                PROD_LINE_POLYX: 'Polyx',
                PROD_LINE_SFERA: 'Sfera',
                PROD_LINE_ETERIS: 'Èteris',
                PROD_LINE_AIR: 'Air'
            }
        },
        { 
            'id': 'BRAND_LEGRAND',
            'names': {
                'short': 'LG', 
                'long': 'Legrand'
            },
            'lines': {
                PROD_LINE_VELA: 'Vela',
                PROD_LINE_ARTEOR: 'Arteor',
                PROD_LINE_MOSAIC: 'Mosaic',
                PROD_LINE_CELIANE: 'Céliane',
            }
        },
        {   'id': 'BRAND_TEGUI',
            'names': {
                'short': 'TG', 
                'long': 'Tegui', 
            }
        },
        {
            'id': 'BRAND_SHIDEAN',
            'names': {
                'short': 'SH',
                'long': 'Shidean'
            }
        },
        {   
            'id': 'BRAND_LEGRAND_BTICINO',
            'names': {
                'short': 'LGG', 
                'long': 'LegrandBticino' 
            },
        },
        {  
            'id': 'BRAND_ARNOULD',
            'names':{
                'short': 'AR', 
                'long': 'Arnould'
            },
            'lines': {
                PROD_LINE_ESPACE_EVOLUTON: 'Espace Évolution'
            }
        }
    ]
    

    PROD_LINES = (
        'UNDEFINED', 
        None,
        None,
        None,
        'Céliane', 
    )

    PARAMS_KEY = '_PARAMS'

    _VIRT_ID_CHECK_LENIENT = False
    _VIRT_ID_CHECK_STRICT = True

    def __new__(cls, devices, subsystem, params):
        dev_sys = getattr(cls, 'DEVICE_SYSTEM', None)
        sys_who = getattr(subsystem, 'SYSTEM_DIAG_WHO', None)
        if sys_who is None:
            print('PANIC : subsystem %s has no SYSTEM_DIAG_WHO' % (str(subsystem)))
            return None
        if dev_sys is not None and dev_sys != sys_who:
            print('PANIC : subsystem %s, device %d' % (str(subsystem), dev_sys))
            return None
        return json.JSONEncoder.__new__(cls)

    def __init__(self, devices, subsystem, params):
        self._devices = devices
        self._subsystem = subsystem
        self._discovery_lock = threading.RLock()
        self._discovery = False
        self.update_base_data(params)

    def log(self, msg):
        if self._devices is not None:
            self._devices.log(msg)
        else:
            print(msg)

    def queue_for_discovery(self):
        """
        Pushes the device to be discovered.
        Makes sure we only push it once
        """
        self._discovery_lock.acquire()
        if self._devices is None:
            self._discovery_lock.release()
            return False
        
        if self._discovery:
            self._discovery_lock.release()
            return False

        self._discovery = True

        params = {
            'devices': self._devices,
            'device': self
        }

        from ..commands import CmdDiagDeviceByAid
        self._devices._system \
            .monitor.push_task(CmdDiagDeviceByAid, params=params)
        self._discovery_lock.release()

    def update_base_data(self, params):
        self._virt_id = params.get('virt_id', None)
        self._hw_addr = params.get('hw_addr', None)
        if isinstance(self._hw_addr, str):
            # TODO: check if we get an exception
            self._hw_addr = int(self._hw_addr)

    def __str__(self):
        _class = '<%s [%s] ' % (self.__class__.__name__, hex(id(self)))
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
        brand_info = self.BRANDS[bid]
        names = brand_info.get('names', {})
        long_name = names.get('long', None)
        return long_name

    def dump_product_line(self):
        bid = getattr(self, '_brand_id', None)
        pln = getattr(self, '_product_line', None)
        if bid is None or pln is None:
            return pln
        if not isinstance(bid, int) or not isinstance(pln, int):
            return pln
        brand_info = self.BRANDS[bid]
        lines = brand_info.get('lines')
        if pln not in lines.keys():
            return pln
        pln_s = lines[pln]
        if pln_s is None:
            return pln
        return pln_s

    def dump_slots(self):
        slots = getattr(self, '_slots', None)
        return slots

    def __to_json__(self):
        data = {}
        data['virt_id'] = self._virt_id
        data['hw_addr'] = self._devices.format_hw_addr(self._hw_addr)

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

        data['subsystem'] = str(self._subsystem)

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
               self._hw_addr is not None

    @property
    def hw_addr(self):
        return self._hw_addr

    def _virt_id_check(self, virt_id, strict=True):
        _virt_id = getattr(self, '_virt_id', None)
        if not strict:
            if _virt_id is None:
                # probably not configured yet, ok
                return True
        if _virt_id != virt_id:
            error_msg = 'this device\'s virt_id is %s, doesn\'t match with %s' \
                        % (self._virt_id, virt_id)
            self.log(error_msg)
            return False
        return True

    def res_object_model(self, virt_id, model_id, nb_conf, brand_id, prod_line):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_LENIENT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            from . import DeviceTypes
            for d in DeviceTypes:
                mid = getattr(d, 'MODEL_ID', None) 
                if mid is not None and mid == model_id:
                    nd = d(self._devices, self._subsystem, {'virt_id': self._virt_id, 'hw_addr': self._hw_addr})
                    # object creation may fail if we're in the wrong subsystem,
                    # continue looking for other devices that may fit better
                    if nd is not None:
                        nd.res_object_model(virt_id, model_id, nb_conf, brand_id, prod_line)
                        self._devices.replace_active_device(nd)
                        return True
            # couldn't find a proper model id
            self._model_id = model_id
            return False
        self._configurators = [0] * nb_conf
        self._brand_id = brand_id
        self._product_line = prod_line
        return True

    def res_fw_version(self, virt_id, fw_version):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_LENIENT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set the firmware version on a BaseDevice instance')
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
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_LENIENT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set configurators 1 through 6 on a BaseDevice instance')
            return False
        # limit the range to the actual number of configurators
        range_max = min(len(self._configurators), 6)
        for i in range(0, range_max):
            v = conf_1_6[i]
            if not self.set_configurator(i, v):
                self.log('Unable to set configurator %d to value %d' % (i, v))
        return True

    def _slots_check(self, slot_id):
        slots = getattr(self, '_slots', [])
        # slot ids start at 1
        if slot_id < 1:
            self.log('slot_set_value : slot_id %d invalid' % (slot_id))
        if slot_id > 32:
            self.log('slot_set_value : slot_id %d appears too large' % (slot_id))
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
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set keyo and state on a BaseDevice instance')
            return False
        self.slot_set_value(slot, 'keyo', keyo)
        self.slot_set_value(slot, 'state', state)
        return True

    def res_ko_sys(self, virt_id, slot, sys, addr):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set sys and addr on a BaseDevice instance')
            return False
        self.slot_set_value(slot, 'sys', sys)
        self.slot_set_value(slot, 'addr', addr)
        return True

    def res_param_ko(self, virt_id, slot, index, val_par):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set parameter on a BaseDevice instance')
            return False
        self.slot_set_param(slot, index, val_par)
        return True

    def end_config_read(self):
        self._discovery = False
        return