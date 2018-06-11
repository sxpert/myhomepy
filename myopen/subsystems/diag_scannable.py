# -*- coding: utf-8 -*-
import sys

from core.logger import LOG_ERROR

from .subsystem import OWNSubSystem

__fname__ = lambda n=0: sys._getframe(n + 1).f_code.co_name

class DiagScannable(OWNSubSystem):
    SYSTEM_IS_SCANNABLE = True

    # scan ops
    OP_CMD_DIAG_ID = 0
    # config ops
    OP_CMD_CONF_ID = 10

    SCAN_CALLBACKS = {
        'CMD_CONF_ID': OP_CMD_CONF_ID,
        'CMD_DIAG_ID': OP_CMD_DIAG_ID,
    }

    SCAN_REGEXPS = {
        'COMMAND': [
            # cmd_conf_abort
            # device abort configuration
            # *[who]*3*0##
            # in reality : the gateway is busy doing stuff on the bus, probably...
            {
                'name': 'CMD_CONF_ABORT',
                're': r'^\*3\*0##$', 
                'func': '_diag_busy'
            },

            # res_trans_end
            # end of transmission from device
            # *[who]*4*[_junk]##
            {
                'name': 'RES_TRANS_END',
                're': r'^\*4\*(?P<_junk>.*)##$',
                'func': '_diag_res_trans_end'
            },

            # cmd_diag_abort
            # programmer abort diagnostic
            # *[who]*6*0##
            {
                'name': 'CMD_DIAG_ABORT',
                're': r'^\*6\*0##$', 
                'func': '_diag_cmd_diag_abort'
            },

            # cmd_conf_id
            # programmer start configuration session with ID
            # *[WHO]*9#[ID]*0##
            {
                'name': 'CMD_CONF_ID',
                're': r'\*9#(?P<hw_addr>\d{1,10})\*0##',
                'func': 'diag_cmd_conf_id'
            },

            # cmd_diag_id
            # programmer starts a diagnostic session wth ID
            # *[who]*10#[id]*0##
            {
                'name': 'CMD_DIAG_ID',
                're': r'^\*10#(?P<hw_addr>\d{1,10})\*0##$', 
                'func': '_diag_cmd_diag_id'
            },

            # cmd_scan_check
            {
                'name': 'CMD_SCAN_CHECK',
                're': r'^\*11#(?P<hw_addr>\d{1,10})\*0##$', 
                'func': '_cmd_scan_check'
            },

            # scanning subsystem reset
            {
                'name': 'CMD_RESET',
                're': r'^\*12\*0##$', 
                'func': '_subsystem_scan_reset'
            },

        ],
        'STATUS': [
            # res_object_model
            # device answers with it's object model and number of physical
            # configurators
            # *#[who]*[where]*1*[object_model]*[n_conf]*[brand]*[line]##
            {
                'name': 'RES_OBJECT_MODEL',
                're': r'^\*(?P<virt_id>\d{1,4})\*1\*(?P<model_id>\d{1,3})\*(?P<nb_conf>\d{1,2})\*(?P<brand_id>\d)\*(?P<prod_line>\d)##$',
                'func': '_diag_res_object_model'
            },

            # res_fw_version
            # device answers with it's firmware version
            # *#[who]*[where]*2*[fw_version]##
            {   
                'name': 'RES_FW_VERSION',
                're': r'^\*(?P<virt_id>\d{1,4})\*2\*(?P<fw_version>.*)##$',
                'func': 'diag_res_fw_version'
            },

            # res_conf_1_6
            # device answers with hardware configurators 1 through 6
            # *#[who]*[where]*4*[c1]*[c2]*[c3]*[c4]*[c5]*[c6]##
            {
                'name': 'RES_CONF_1_6',
                're': r'^\*(?P<virt_id>\d{1,4})\*4\*(?P<c1>\d{1,3})\*(?P<c2>\d{1,3})\*(?P<c3>\d{1,3})\*(?P<c4>\d{1,3})\*(?P<c5>\d{1,3})\*(?P<c6>\d{1,3})##$',
                'func': '_diag_res_conf_1_6'
            },

            # res_conf_7_12
            # device answers with hardware configurators 7 through 12
            # *#[who]*[where]*5*[c7]*[c8]*[c9]*[c10]*[c11]*[c12]##
            {
                'name': 'RES_CONF_7_12',
                're': r'^\*(?P<virt_id>\d{1,4})\*5\*(?P<c7>\d{1,3})\*(?P<c8>\d{1,3})\*(?P<c9>\d{1,3})\*(?P<c10>\d{1,3})\*(?P<c11>\d{1,3})\*(?P<c12>\d{1,3})##$', 
                'func': '_diag_res_conf_7_12'
            },

            # res_diag_a
            # device answers with diagnostic bit set A
            # *#[who]*[where]*7*[bitmask_dia_a]##
            {
                'name': 'RES_DIAG_A',
                're': r'^\*(?P<virt_id>\d{1,4})\*7\*(?P<diag_bits>[01]{24})##$',
                'func': '_diag_res_diag_a'
            },

            # res_diag_b
            # device answers with diagnostic bit set B
            # *#[who]*[where]*8*[bitmask_dia_a]##
            {
                'name': 'RES_DIAG_B',
                're': r'^\*(?P<virt_id>\d{1,4})\*8\*(?P<diag_bits>[01]{24})##$',
                'func': '_diag_res_diag_b'
            },

            # device diagnostics
            # see notes.txt
            {
                'name': 'WARN_DEVICE_DIAG',
                're': r'^\*(?P<virt_id>\d{1,4})\*11\*(?P<diag_bits>[01]{24})##$',
                'func': '_analyze_diagnostics'
            },

            # res_id
            # device answers with it's ID
            # *#[who]*[where]*13*[id]##
            {
                'name': 'DIAG_RES_ID',
                're': r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$',
                'func': '_diag_res_id'
            },
            # res_ko_value
            # device answers with it's key/object, value and state
            # *#[who]*[where]*30*[slot]*[keyo]*[state]##
            {
                'name': 'RES_KO_VALUE',
                're': r'^\*(?P<virt_id>\d{1,4})\*30\*(?P<slot>\d{1,3})\*(?P<keyo>\d{1,5})\*(?P<state>[01])##$',
                'func': 'diag_res_ko_value'
            },

            # cmd_ko_value
            # programmer send the configuration of key_object value
            # *#[WHO]*0*#30*[SLOT]*[KEYO]##
            {
                'name': 'CMD_KO_VALUE',
                're': r'^\*0\*#30\*(?P<slot>\d{1,3})\*(?P<keyo>\d{1,5})##$',
                'func': 'diag_cmd_ko_value'
            },

            # res_ko_sys
            # device answers with it's key/object, system and address",
            # *#[who]*[where]*32#[slot]*[sys]*[addr]##
            {
                'name': 'RES_KO_SYS',
                're': r'^\*(?P<virt_id>\d{1,4})\*32#(?P<slot>\d{1,3})\*(?P<sys>\d{1,3})\*(?P<addr>\d{1,5})##$',
                'func': 'diag_res_ko_sys'
            },

            # cmd_ko_sys
            # programmer send the configuration of key_object, system and address
            # *#[WHO]*0*#32#[SLOT]*[SYS]*[ADDR]##
            {
                'name': 'CMD_KO_SYS',
                're': r'^\*0\*#32#(?P<slot>\d{1,3})\*(?P<sys>\d{1,3})\*(?P<addr>\d{1,5})##$',
                'func': 'diag_cmd_ko_sys'
            },            

            # res_param_ko
            # device answers with the key/value of key/object
            # *#[who]*[where]*35#[index]#[slot]*[val_par]##
            {
                'name': 'RES_PARAM_KO',
                're': r'\*(?P<virt_id>\d{1,4})\*35#(?P<index>\d{1,3})#(?P<slot>\d{1,3})\*(?P<val_par>\d{1,5})##',
                'func': 'diag_res_param_ko'
            },

            # cmd_param_ko
            # programmer send the configuration of the parameters of ko
            # *#[WHO]*0*#35#[INDEX]#[SLOT]*[VAL_PAR]##
            {
                'name': 'CMD_PARAM_KO',
                're': r'\*0\*#35#(?P<index>\d{1,3})#(?P<slot>\d{1,3})\*(?P<value>\d{1,5})##',
                'func': 'diag_cmd_param_ko'
            }
        ]
    }

    # ---------------------------------------------------------------------
    #
    # Message parsing stuff
    #

    def parse_regexp(self, msg):
        sys_regexps = self.get_regexps(msg, 'SYSTEM_REGEXPS')
        scan_regexps = self.get_regexps(msg, 'SCAN_REGEXPS')
        regexps = sys_regexps + scan_regexps
        return self._parse_regexp(msg, regexps)

   # ---------------------------------------------------------------------
    #
    # Callback stuff
    #

    def map_callback_name(self, name):
        self.log('DiagScannable.map_callback_name')
        scan_callbacks = getattr(self, 'SCAN_CALLBACKS', None)
        sys_callbacks = getattr(self, 'SYSTEM_CALLBACKS', None)
        _cb = scan_callbacks.copy()
        self.log(_cb)
        if sys_callbacks is not None:
            _cb.update(sys_callbacks)
        _cb_name = self.__class__._map_callback_name(name, _cb)
        self.log(_cb_name)
        return _cb_name

    def map_device(self, device):
        self.log('DiagScannable.map_device : %s' % (str(device)))
        if device is None:
            return '*'
        return str(device)

    # ---------------------------------------------------------------------
    #
    # SubSystem-specific functions
    #

    def _diag_busy(self, matches):
        return True

    def _diag_res_trans_end(self, matches):

        def end_of_transmission_event():
            res = self.system.devices.eot_event(self, matches)
            if not res:
                self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return False
            return True

        return end_of_transmission_event

    def _diag_cmd_diag_abort(self, matches):

        def end_of_configuration():
            self.log('Signaling the end of configuration')
            self.system.devices.end_config_read()
            self.system.devices.reset_active_device()
            return True

        return end_of_configuration

    def diag_cmd_conf_id(self, matches):
        hw_addr = int(matches.get('hw_addr', None))

        def cmd_conf_id():
            try:
                res = self.system.devices.cmd_conf_id(hw_addr, self)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res

        info = {
            'data': {
                'hw_addr': hw_addr
            },
            'device': None,
            'order': self.OP_CMD_CONF_ID,
            'func': cmd_conf_id
        }
        return info

    def diag_cmd_diag_id(self, matches):
        hw_addr = int(matches.get('hw_addr', None))
        
        def cmd_diag_id():
            res = self.system.devices.cmd_diag_id(hw_addr, self)
            if not res:
                self.log('FAILED: %s %s' % (__fname__(), str(matches)))
            return res
        
        info = {
            'data': {
                'hw_addr': hw_addr 
            },
            'device': None,
            'order': self.OP_CMD_DIAG_ID,
            'func': cmd_diag_id
        }
        return info

    def _cmd_scan_check(self, matches):
        return True

    def _subsystem_scan_reset(self, matches):
        # self.log('scan reset for %d subsystem' % self.SYSTEM_WHO)
        return True

    def _diag_res_object_model(self, matches):
        _virt_id = matches['virt_id']
        _model_id = int(matches['model_id'])
        _nb_conf = int(matches['nb_conf'])
        _brand_id = int(matches['brand_id'])
        _prod_line = int(matches['prod_line'])
        res = self.system.devices.res_object_model(_virt_id, _model_id,
                                                   _nb_conf, _brand_id,
                                                   _prod_line)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def parse_version(self, version):
        if version[-1] != '*':
            version += '*'
        names = ('major', 'minor', 'build')
        ver = {}
        var = ''
        cur = 0
        for c in version:
            if c.isdecimal():
                var += c
            elif c == '*':
                if cur < len(names):
                    k = names[cur]
                else:
                    k = cur
                ver[k] = int(var)
                var = ''
                cur += 1
        return ver

    def diag_res_fw_version(self, matches):
        virt_id = matches['virt_id']
        fw_ver = self.parse_version(matches['fw_version'])
        res = self.system.devices.res_fw_version(virt_id, fw_ver)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def _diag_res_conf_1_6(self, matches):
        _virt_id = matches['virt_id']
        _c1 = int(matches['c1'])
        _c2 = int(matches['c2'])
        _c3 = int(matches['c3'])
        _c4 = int(matches['c4'])
        _c5 = int(matches['c5'])
        _c6 = int(matches['c6'])
        _c_1_6 = (_c1, _c2, _c3, _c4, _c5, _c6, )
        res = self.system.devices.res_conf_1_6(_virt_id, _c_1_6)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def _diag_res_conf_7_12(self, matches):
        _virt_id = matches['virt_id']
        _c7 = int(matches['c7'])
        _c8 = int(matches['c8'])
        _c9 = int(matches['c9'])
        _c10 = int(matches['c10'])
        _c11 = int(matches['c11'])
        _c12 = int(matches['c12'])
        _c_7_12 = (_c7, _c8, _c9, _c10, _c11, _c12, )
        res = self.system.devices.res_conf_7_12(_virt_id, _c_7_12)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def _diag_res_diag_a(self, matches):
        self.log('res_diag_a %s' % (str(matches)))
        return True

    def _analyze_diagnostics(self, matches):
        self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return True

    def _diag_res_id(self, matches):
        # self.log('res_id %s' % str(matches))
        _virt_id = matches['virt_id']
        _hw_addr = matches['hw_addr']
        hw_addr_x = self.system.devices.format_hw_addr(_hw_addr)

        def register():
            dev = self.system.devices.register(self, matches)
            if dev is None:
                self.log('Unable to register device with virt_id %s and hw_addr %s' % (_virt_id, hw_addr_x))
                return False
            return True

        return register

    def diag_res_ko_value(self, matches):
        virt_id = matches['virt_id']
        slot = int(matches['slot'])
        keyo = int(matches['keyo'])
        state = int(matches['state'])

        def res_ko_value():
            res = self.system.devices.res_ko_value(virt_id, slot, keyo, state)
            if not res:
                self.log('FAILED: %s %s' % (__fname__(), str(matches)))
            return res
        
        return res_ko_value

    def diag_res_ko_sys(self, matches):
        virt_id = matches['virt_id']
        slot = int(matches['slot'])
        sys = int(matches['sys'])
        addr = matches['addr']

        def res_ko_sys():
            res = self.system.devices.res_ko_sys(virt_id, slot, sys, addr)
            if not res:
                self.log('FAILED: %s %s' % (__fname__(), str(matches)))
            return res

        return res_ko_sys

    def diag_cmd_ko_sys(self, matches):
        slot = int(matches['slot'])
        sys = int(matches['sys'])
        addr = matches['addr']

        def cmd_ko_sys():
            try:
                res = self.system.devices.cmd_ko_sys(slot, sys, addr)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
            
        return cmd_ko_sys

    def diag_res_param_ko(self, matches):
        virt_id = matches['virt_id']
        slot = int(matches['slot'])
        index = int(matches['index'])
        value = int(matches['val_par'])

        def res_param_ko():
            try:
                res = self.system.devices.res_param_ko(virt_id, slot, index, value)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res

        return res_param_ko

    def diag_cmd_param_ko(self, matches):
        slot = int(matches['slot'])
        index = int(matches['index'])
        value = int(matches['value'])

        def cmd_param_ko():
            try:
                res = self.system.devices.cmd_param_ko(slot, index, value)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res

        return cmd_param_ko
