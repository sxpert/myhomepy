# -*- coding: utf-8 -*-

import json
import asyncio

from core.logger import LOG_ERROR, LOG_DEBUG
from myopen.subsystems import DiagScannable, find_subsystem
from myopen.constants import (
    CONST_DEVICE_ICON, VAR_ICON,
    VAR_SYSTEM_DIAG_WHO, VAR_SYSTEM_NAME, VAR_MODEL_ID,
    VAR_SLOTS, VAR_DEVICE_SYSTEM,)
from .slots import (
    Slots
)


class BaseDevice(object):
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
            'names': {'short': '_', 'long': 'Undefined'},
            'note': 'Lots of devices have no brand specified, '
                    'in particular older devices',
            'lines': {
                PROD_LINE_UNDEFINED: 'Undefined'
            }
        },
        {
            'id': 'BRAND_BTICINO',
            'names': {'short': 'BT', 'long': 'BTicino'},
            'note': 'Italian originated brand, global market',
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
            'names': {'short': 'LG', 'long': 'Legrand'},
            'note': 'French originated brand, global market',
            'lines': {
                PROD_LINE_VELA: 'Vela',
                PROD_LINE_ARTEOR: 'Arteor',
                PROD_LINE_MOSAIC: 'Mosaic',
                PROD_LINE_CELIANE: 'Céliane',
            }
        },
        {
            'id': 'BRAND_TEGUI',
            'names': {'short': 'TG', 'long': 'Tegui'},
            'note': 'Spanish originated brand'
        },
        {
            'id': 'BRAND_SHIDEAN',
            'names': {'short': 'SH', 'long': 'Shidean'},
            'note': 'Chinese brand, south asia market ?'
        },
        {
            'id': 'BRAND_LEGRAND_BTICINO',
            'names': {'short': 'LGG', 'long': 'LegrandBticino'},
            'note': 'Global brand'
        },
        {
            'id': 'BRAND_ARNOULD',
            'names': {'short': 'AR', 'long': 'Arnould'},
            'note': 'High level brand, french market',
            'lines': {
                PROD_LINE_ESPACE_EVOLUTON: 'Espace Évolution'
            }
        }
    ]

    _VIRT_ID_CHECK_LENIENT = False
    _VIRT_ID_CHECK_STRICT = True

    def __init__(self, devices, subsystem, params):
        self.devices = devices
        self.log = devices.log

        # front-end related things
        self._name = None
        self._description = None
        
        # device things
        self._virt_id = None
        self._hw_addr = None

        # if we get the diag_* subsystem here, find the
        # right one
        sys_diag_who = getattr(subsystem, VAR_SYSTEM_DIAG_WHO, None)
        if sys_diag_who is not None:
            # we have the diag_* subsystem
            # get the right class of device
            subsystem = find_subsystem(sys_diag_who)
        self.subsystem = subsystem
        self._discovery = False
        self._error = not self.update_base_data(params)
        self.slots = Slots(self)

    def queue_for_discovery(self, callback=None):
        """
        Pushes the device to be discovered.
        Makes sure we only push it once
        """
        if self.devices is None:
            self.log('devices is None', LOG_ERROR)
            return False

        if self._discovery:
            self.log('already set for discovery', LOG_ERROR)
            return False

        self._discovery = True

        params = {
            'devices': self.devices,
            'device': self
        }

        if self.devices.system.has_task_queue:
            from ..commands.asyncio_cmd_diag_aid import CmdDiagAid
            # if self.devices.format_hw_addr(self.hw_addr) == '0095F706':
            # self.log('BaseDevice.queue_for_discovery : '
            #          'CmdDiagAid %s'
            #          % (str(params)),
            #          LOG_ERROR)
            self.devices.system.push_task(CmdDiagAid, params=params, callback=callback)
        else:
            self.log('BaseDevice.queue_for_discovery : no main loop, not doing anything')

    def update_base_data(self, params):
        self._virt_id = params.get('virt_id', None)
        self._hw_addr = params.get('hw_addr', None)
        if isinstance(self._hw_addr, str):
            # TODO: check if we get an exception
            if self._hw_addr.isdecimal():
                self._hw_addr = int(self._hw_addr)
        return True

    def __str__(self):
        _class = '<%s [%s] ' % (self.__class__.__name__, hex(id(self)))
        if self.subsystem is not None:
            _class += '%s ' % (str(self.subsystem))
        brand_name = self.dump_brand()
        if brand_name is not None:
            _class += '%s ' % (brand_name)
            line_name = self.dump_product_line()
            if line_name is not None:
                _class += '%s ' % (line_name)
        fw = self.fw_version
        if fw is not None:
            _class += 'fw:%s ' % (fw)
        confs = self.dump_configurators()
        if confs is not None:
            _class += '%s ' % (str(confs))
        if self.valid:
            from . import Devices
            return '%sid: %s>' % (_class, Devices.format_hw_addr(self._hw_addr))
        return '%sINVALID>' % (_class)

    # ========================================================================
    #
    # web frontend related functionnality
    #
    # ========================================================================

    @property
    def valid(self):
        return self.subsystem is not None and \
               self._hw_addr is not None

    @property
    def hw_addr(self):
        return self._hw_addr

    @property
    def hw_addr_hex(self):
        return '%08X' % (self._hw_addr)

    @property
    def icon(self):
        icon = getattr(self, VAR_ICON, None)
        if icon is None:
            return CONST_DEVICE_ICON
        return icon

    @property
    def name(self):
        name = getattr(self, '_name', None)
        if name is None:
            name = ''
        return name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        description = getattr(self, '_description', None)
        if description is None:
            description = ''
        return description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def brand_id(self):
        brand_id = self._brand_id
        brand = self.BRANDS[brand_id]
        return brand['id']

    @property
    def product_line(self):
        return self._product_line

    @property
    def model_id(self):
        mid = getattr(self, VAR_MODEL_ID, None)
        if mid is not None:
            return mid
        # if the model wasn't known, this may be available
        if mid is None:
            mid = getattr(self, '_model_id', None)
            if mid is not None:
                return mid
        self.log('unable to find device\'s model_id %s' % self, LOG_ERROR)
        return mid
        
    @property
    def web_data(self):
        """
        this generates a dictionary of what the frontend requires 
        to show the device configuration page
        """
        data = {}
        data['id'] = self.hw_addr_hex
        data['name'] = self.name
        data['description'] = self.description
        data['brand_id'] = self.brand_id
        data['product_line'] = self.product_line
        data['subsystem'] = self.dump_subsystem()
        data['model_id'] = self.model_id
        data['slots'] = self.slots.web_data
        return data

    # ========================================================================
    #
    # brands and product lines handling
    #
    # ========================================================================

    def find_brand_id(self, brand_id):
        if isinstance(brand_id, str):
            if brand_id.isnumeric():
                brand_id = int(brand_id)
                if brand_id > 0 and brand_id < len(self.BRANDS):
                    return brand_id
                return None
            else:
                for brand_num in range(0, len(self.BRANDS)):
                    brand_data = self.BRANDS[brand_num]
                    brand_id_label = brand_data.get('id', None)
                    if brand_id_label is not None and \
                       brand_id_label == brand_id:
                        return brand_num
                    names = brand_data.get('names', None)
                    if names is not None:
                        short_name = names.get('short', None)
                        if short_name is not None and short_name == brand_id:
                            return brand_num
                        long_name = names.get('long', None)
                        if long_name is not None and long_name == brand_id:
                            return brand_num
        return None

    def set_brand_id(self, brand_id):
        brand_num = self.find_brand_id(brand_id)
        if brand_num is not None:
            self._brand_id = brand_num

    def find_product_line(self, product_line):
        brand_info = self.BRANDS[self._brand_id]
        lines = brand_info.get('lines', None)
        if lines is None:
            return None
        for k in lines.keys():
            v = lines[k]
            if v == product_line:
                return k
        return None

    def set_product_line(self, product_line):
        line_num = self.find_product_line(product_line)
        if line_num is not None:
            self._product_line = line_num

    # ========================================================================
    #
    # load from json representation
    #
    # ========================================================================

    def loads(self, data):
        if not isinstance(data, dict):
            self.log('devices should contain a list', LOG_ERROR)
            return None

        confs = data.get('configurators', None)
        if confs is not None:
            self._configurators = confs

        brand_id = data.get('brand_id', None)
        if brand_id is not None:
            self.set_brand_id(brand_id)
            # line_id can only make sense if we have a brand
            product_line = data.get('product_line', None)
            if product_line is not None:
                self.set_product_line(product_line)
        fw = data.get('firmware_version', None)
        if fw is not None:
            self._fw_version = fw

        model_id = data.get('model_id', None)

        if self.__class__ is not BaseDevice:
            # time to load slots
            slots = data.get('slots', None)
            if slots is not None and isinstance(slots, list):
                if not self.slots.loads(slots):
                    self.log('BaseDevice.loads ERROR : unable to load slots %s' % (str(slots)), LOG_ERROR)
                self.log('slots -> %s' % (str(self.slots)), LOG_DEBUG)
            return self

        if model_id is None:
            return self

        dc = self.find_device_class(model_id)
        if dc is None:
            self.log('unable to find appropriate class for model_id %d' % (model_id), LOG_ERROR)
            return self
        nd = dc(self.devices, self.subsystem, data)
        if nd.__class__ != BaseDevice:
            nd.loads(data)
        return nd

    # def load_slot(self, sid, slot_data):
    #     return slot_data

    def dump_subsystem(self):
        subsystem_id = self.subsystem.SYSTEM_WHO
        if issubclass(self.subsystem.__class__, DiagScannable):
            subsystem_id = self.subsystem.SYSTEM_DIAG_WHO
        # try to find a name
        subs = find_subsystem(subsystem_id)
        subsystem_name = getattr(subs, VAR_SYSTEM_NAME, None)
        res = subsystem_id
        if subsystem_name is not None:
            res = subsystem_name
        if not isinstance(res, str):
            res = str(res)
        return res

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

    @property
    def fw_version(self):
        fw = getattr(self, '_fw_version', None)
        if fw is not None:
            fw = '%d.%d.%d' % (fw['major'], fw['minor'], fw['build'])
        return fw

    def __to_json__(self):
        data = {}
        data['virt_id'] = self._virt_id
        data['hw_addr'] = self.devices.format_hw_addr(self._hw_addr)

        # MODEL_ID handling
        # the proper model_id
        model_id = getattr(self, VAR_MODEL_ID, None)
        if model_id is not None:
            data['model_id'] = model_id
        # if the model wasn't known, this may be available
        if model_id is None:
            model_id = getattr(self, '_model_id', None)
            if model_id is not None:
                data['_model_id'] = model_id

        data['subsystem'] = self.dump_subsystem()

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

        data[VAR_SLOTS] = self.slots
        return data

    # ========================================================================
    #
    # callbacks used by the configuration system in the bus
    #
    # ========================================================================

    def _virt_id_check(self, virt_id, strict=True):
        _virt_id = getattr(self, '_virt_id', None)
        if not strict:
            if _virt_id is None:
                # probably not configured yet, ok
                return True
        if _virt_id != virt_id:
            error_msg = 'this device\'s virt_id is %s, doesn\'t match with %s' % (self._virt_id, virt_id)
            self.log(error_msg, LOG_ERROR)
            return False
        return True

    def find_device_class(self, model_id):
        from . import DeviceTypes
        for dt in DeviceTypes:
            mss = getattr(dt, VAR_DEVICE_SYSTEM, None)
            if mss is None:
                continue
            mid = getattr(dt, VAR_MODEL_ID, None)
            if mid is None:
                continue
            if mss is self.subsystem and mid == model_id:
                return dt
        return None

    def res_object_model(self, virt_id, model_id,
                         nb_conf, brand_id, prod_line):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_LENIENT):
            return False
        if self.__class__ == BaseDevice:
            dc = self.find_device_class(model_id)
            if dc is not None:
                nd = dc(self.devices, self.subsystem, {'virt_id': self._virt_id, 'hw_addr': self._hw_addr})
                if nd is not None:
                    nd.res_object_model(virt_id, model_id, nb_conf, brand_id, prod_line)
                    self.devices.replace_active_device(nd)
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

    def res_conf_7_12(self, virt_id, conf_7_12):
        # not implemented yet
        return False

    def res_ko_value(self, virt_id, slot, keyo, state):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set keyo and state on a BaseDevice instance')
            return False
        return self.slots.res_ko_value(slot, keyo, state)

    def res_ko_sys(self, virt_id, slot, sys, addr):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set sys and addr on a BaseDevice instance')
            return False
        return self.slots.res_ko_sys(slot, sys, addr)

    def res_param_ko(self, virt_id, slot, index, val_par):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        if self.__class__.__name__ == BaseDevice.__name__:
            self.log('can\'t set parameter on a BaseDevice instance')
            return False
        return self.slots.res_param_ko(slot, index, val_par)

    def end_config_read(self):
        self._discovery = False
        return
