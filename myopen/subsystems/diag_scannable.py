# -*- coding: utf-8 -*-
import sys

from core.logger import LOG_ERROR

from .subsystem import OWNSubSystem

__fname__ = lambda n=0: sys._getframe(n + 1).f_code.co_name

class DiagScannable(OWNSubSystem):
    SYSTEM_IS_SCANNABLE = True

    OP_CMD_CONF_END =       2
    OP_CMD_CONF_ABORT =     3
    OP_CMD_DIAG_ABORT =     6
    OP_CMD_CONF_ID =        9
    OP_CMD_DIAG_ID =       10
    OP_CMD_SCAN_CHECK =    11
    OP_CMD_RESET =         12
    OP_CMD_RESET_ALL_KO =  14
    OP_CMD_RESET_KO =     114
    OP_RES_CONF_OK =       52
    OP_RES_TRANS_END =   1004
    OP_RES_ID =          1013
    OP_RES_KO_VALUE =    1030
    OP_RES_KO_SYS =      1032
    OP_RES_PARAM_KO =    1035
    OP_CMD_KO_VALUE =    1130
    OP_CMD_KO_SYS =      1132
    OP_CMD_PARAM_KO =    1135

    SCAN_CALLBACKS = {
        'CMD_CONF_END':     OP_CMD_CONF_END,
        'CMD_CONF_ABORT':   OP_CMD_CONF_ABORT,
        'CMD_DIAG_ABORT':   OP_CMD_DIAG_ABORT,
        'CMD_CONF_ID':      OP_CMD_CONF_ID,
        'SCAN_CMD_DIAG_ID': OP_CMD_DIAG_ID,
        'CMD_DIAG_ID':      OP_CMD_DIAG_ID,
        'CMD_SCAN_CHECK':   OP_CMD_SCAN_CHECK,
        'CMD_RESET':        OP_CMD_RESET,
        'CMD_RESET_ALL_KO': OP_CMD_RESET_ALL_KO,
        'CMD_RESET_KO':     OP_CMD_RESET_KO,
        'RES_CONF_OK':      OP_RES_CONF_OK,

        'RES_TRANS_END':    OP_RES_TRANS_END,
        'RES_ID':           OP_RES_ID,
        'RES_KO_VALUE':     OP_RES_KO_VALUE,
        'RES_KO_SYS':       OP_RES_KO_SYS,
        'RES_PARAM_KO':     OP_RES_PARAM_KO,
        'CMD_KO_VALUE':     OP_CMD_KO_VALUE,
        'CMD_KO_SYS':       OP_CMD_KO_SYS,
        'CMD_PARAM_KO':     OP_CMD_PARAM_KO,
    }

    SCAN_REGEXPS = {
        'COMMAND': [

            # cmd_conf_end
            # programmer send end of configuration
            # *[WHO]*2*0##
            {
                'name': 'CMD_CONF_END',
                're': r'^\*2\*0##$',
                'func': 'diag_cmd_conf_end'
            },

            # cmd_conf_abort
            # device abort configuration
            # *[who]*3*0##
            # Note: in reality : the gateway is busy doing stuff on the bus, probably...
            {
                'name': 'CMD_CONF_ABORT',
                're': r'^\*3\*0##$', 
                'func': 'diag_cmd_conf_abort'
            },

            # res_trans_end
            # end of transmission from device
            # *[who]*4*[_junk]##
            {
                'name': 'RES_TRANS_END',
                're': r'^\*4\*(?P<_junk>.*)##$',
                'func': 'diag_res_trans_end'
            },

            # cmd_diag_abort
            # programmer abort diagnostic
            # *[who]*6*0##
            {
                'name': 'CMD_DIAG_ABORT',
                're': r'^\*6\*0##$', 
                'func': 'diag_cmd_diag_abort'
            },

            # cmd_conf_id
            # programmer start configuration session with ID
            # *[WHO]*9#[ID]*0##
            {
                'name': 'CMD_CONF_ID',
                're': r'^\*9#(?P<hw_addr>\d{1,10})\*0##$',
                'func': 'diag_cmd_conf_id'
            },

            # cmd_diag_id
            # programmer starts a diagnostic session wth ID
            # *[who]*10#[id]*0##
            {
                'name': 'CMD_DIAG_ID',
                're': r'^\*10#(?P<hw_addr>\d{1,10})\*0##$', 
                'func': 'diag_cmd_diag_id'
            },

            # cmd_scan_check
            # programmer send flag to all the devices found
            # Note: no idea what the hell this does...
            # *[WHO]*11#[ID]*0##
            {
                'name': 'CMD_SCAN_CHECK',
                're': r'^\*11#(?P<hw_addr>\d{1,10})\*0##$', 
                'func': 'diag_cmd_scan_check'
            },

            # cmd_reset
            # programmer delete from memory the previous scans
            # *[WHO]*12*0##
            {
                'name': 'CMD_RESET',
                're': r'^\*12\*0##$', 
                'func': 'diag_cmd_reset'
            },

            # cmd_reset_all_ko
            # programmer reset all KO of device
            # *[WHO]*14#0*0##
            # cmd_reset_ko
            # programmer reset a specific KO of device
            # *[WHO]*14#[SLOT]*0##
            {
                'name': 'CMD_RESET_KO',
                're': r'^\*14#(?P<slot>\d{1,3})\*0##$',
                'func': 'diag_cmd_reset_ko'
            },

            # res_conf_ok
            # device answer configuration ok
            # *[WHO]*52*[_junk]##
            {
                'name': 'RES_CONF_OK',
                're': r'^\*52\*(?P<_junk>.*)##$',
                'func': 'diag_res_conf_ok'
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
                'func': 'diag_res_object_model'
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
                'func': 'diag_res_conf_1_6'
            },

            # res_conf_7_12
            # device answers with hardware configurators 7 through 12
            # *#[who]*[where]*5*[c7]*[c8]*[c9]*[c10]*[c11]*[c12]##
            {
                'name': 'RES_CONF_7_12',
                're': r'^\*(?P<virt_id>\d{1,4})\*5\*(?P<c7>\d{1,3})\*(?P<c8>\d{1,3})\*(?P<c9>\d{1,3})\*(?P<c10>\d{1,3})\*(?P<c11>\d{1,3})\*(?P<c12>\d{1,3})##$', 
                'func': 'diag_res_conf_7_12'
            },

            # res_diag_a
            # device answers with diagnostic bit set A
            # *#[who]*[where]*7*[bitmask_dia_a]##
            {
                'name': 'RES_DIAG_A',
                're': r'^\*(?P<virt_id>\d{1,4})\*7\*(?P<diag_bits>[01]{24})##$',
                'func': 'diag_res_diag_a'
            },

            # res_diag_b
            # device answers with diagnostic bit set B
            # *#[who]*[where]*8*[bitmask_dia_a]##
            {
                'name': 'RES_DIAG_B',
                're': r'^\*(?P<virt_id>\d{1,4})\*8\*(?P<diag_bits>[01]{24})##$',
                'func': 'diag_res_diag_b'
            },

            # device diagnostics
            # see notes.txt
            {
                'name': 'WARN_DEVICE_DIAG',
                're': r'^\*(?P<virt_id>\d{1,4})\*11\*(?P<diag_bits>[01]{24})##$',
                'func': 'analyze_diagnostics'
            },

            # res_id
            # device answers with it's ID
            # *#[who]*[where]*13*[id]##
            {
                'name': 'DIAG_RES_ID',
                're': r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$',
                'func': 'diag_res_id'
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
    # helper fuctions
    #

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

    # ---------------------------------------------------------------------
    #
    # SubSystem-specific functions
    #

    def diag_cmd_conf_end(self, matches):
        def cmd_conf_end():
            try:
                res = self.system.devices.cmd_conf_end()
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': None,
            'device': None,
            'order': self.OP_CMD_CONF_END,
            'func': cmd_conf_end
        }
        return info


    def diag_cmd_conf_abort(self, matches):
        """
        supposedly 'res_gw_busy' but it's rather useless, so we just skip it...
        """
        return True

    def diag_res_trans_end(self, matches):
        def res_trans_end():
            try:
                res = self.system.devices.res_trans_end()
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': None,
            'device': None,
            'order': self.OP_RES_TRANS_END,
            'func': res_trans_end
        }
        return info

    def diag_cmd_diag_abort(self, matches):
        """
        should be named 'res_end_of_diagnostic'
        """
        def cmd_diag_abort():
            try:
                res = self.system.devices.cmd_diag_abort()
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': None,
            'device': None,
            'order': self.OP_CMD_DIAG_ABORT,
            'func': cmd_diag_abort
        }
        return info

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
            'data': {'hw_addr': hw_addr},
            'device': None,
            'order': self.OP_CMD_CONF_ID,
            'func': cmd_conf_id
        }
        return info

    def diag_cmd_diag_id(self, matches):
        hw_addr = int(matches.get('hw_addr', None))      
        def cmd_diag_id():
            try:
                res = self.system.devices.cmd_diag_id(hw_addr, self)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res      
        info = {
            'data': {'hw_addr': hw_addr},
            'device': None,
            'order': self.OP_CMD_DIAG_ID,
            'func': cmd_diag_id
        }
        return info

    def diag_cmd_scan_check(self, matches):
        return True

    def diag_cmd_reset(self, matches):
        # self.log('scan reset for %d subsystem' % self.SYSTEM_WHO)
        return True

    def diag_cmd_reset_ko(self, matches):
        slot = int(matches.get('slot', None))
        op = self.OP_CMD_RESET_KO
        data = {'slot': slot}
        if slot == 0: 
            slot = None
            data = None
            op = self.OP_CMD_RESET_ALL_KO
        def cmd_reset_ko():
            try:
                res = self.system.devices.cmd_reset_ko(slot)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': data,
            'device': None,
            'order': op,
            'func': cmd_reset_ko
        }
        return info
                
    def diag_res_conf_ok(self, matches):
        def res_conf_ok():
            try:
                res = self.system.devices.res_conf_ok()
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': None,
            'device': None,
            'order': self.OP_RES_CONF_OK,
            'func': res_conf_ok
        }
        return info      

    def diag_res_object_model(self, matches):
        virt_id = matches['virt_id']
        model_id = int(matches['model_id'])
        nb_conf = int(matches['nb_conf'])
        brand_id = int(matches['brand_id'])
        prod_line = int(matches['prod_line'])
        res = self.system.devices.res_object_model(virt_id, model_id, nb_conf, brand_id, prod_line)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def diag_res_fw_version(self, matches):
        virt_id = matches['virt_id']
        fw_ver = self.parse_version(matches['fw_version'])
        res = self.system.devices.res_fw_version(virt_id, fw_ver)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def diag_res_conf_1_6(self, matches):
        virt_id = matches['virt_id']
        c1 = int(matches['c1'])
        c2 = int(matches['c2'])
        c3 = int(matches['c3'])
        c4 = int(matches['c4'])
        c5 = int(matches['c5'])
        c6 = int(matches['c6'])
        c_1_6 = (c1, c2, c3, c4, c5, c6, )
        res = self.system.devices.res_conf_1_6(virt_id, c_1_6)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def diag_res_conf_7_12(self, matches):
        virt_id = matches['virt_id']
        c7 = int(matches['c7'])
        c8 = int(matches['c8'])
        c9 = int(matches['c9'])
        c10 = int(matches['c10'])
        c11 = int(matches['c11'])
        c12 = int(matches['c12'])
        c_7_12 = (c7, c8, c9, c10, c11, c12, )
        res = self.system.devices.res_conf_7_12(virt_id, c_7_12)
        if not res:
            self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return res

    def diag_res_diag_a(self, matches):
        self.log('res_diag_a %s' % (str(matches)))
        return True

    def diag_res_diag_b(self, matches):
        self.log('res_diag_b %s' % (str(matches)))
        return True

    def analyze_diagnostics(self, matches):
        self.log('FAILED: %s %s' % (__fname__(), str(matches)))
        return True

    def diag_res_id(self, matches):
        virt_id = matches['virt_id']
        hw_addr = matches['hw_addr']
        hw_addr_x = self.system.devices.format_hw_addr(hw_addr)
        def res_id():
            try:
                dev = self.system.devices.register(self, matches)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not dev:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                    return False
                return True
        info = {
            'data': {'virt_id': virt_id, 'hw_addr': hw_addr, 'hw_addr_x': hw_addr_x},
            'device': None,
            'order': self.OP_RES_ID,
            'func': res_id
        }            
        return info

    def diag_res_ko_value(self, matches):
        virt_id = matches['virt_id']
        slot = int(matches['slot'])
        keyo = int(matches['keyo'])
        state = int(matches['state'])
        def res_ko_value():
            try:
                res = self.system.devices.res_ko_value(virt_id, slot, keyo, state)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': {'virt_id': virt_id, 'slot': slot, 'keyo': keyo, 'state': state},
            'device': None,
            'order': self.OP_RES_KO_VALUE,
            'func': res_ko_value
        }            
        return info

    def diag_cmd_ko_value(self, matches):
        slot = int(matches['slot'])
        keyo = int(matches['keyo'])
        def cmd_ko_value():
            try:
                res = self.system.devices.cmd_ko_value(slot, keyo)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': {'slot': slot, 'keyo': keyo},
            'device': None,
            'order': self.OP_CMD_KO_VALUE,
            'func': cmd_ko_value
        }            
        return info

    def diag_res_ko_sys(self, matches):
        virt_id = matches['virt_id']
        slot = int(matches['slot'])
        sys = int(matches['sys'])
        addr = matches['addr']
        def res_ko_sys():
            try:
                res = self.system.devices.res_ko_sys(virt_id, slot, sys, addr)
            except Exception as e:
                self.log('FAILED: %s [%s]' % (__fname__(), str(e)), LOG_ERROR)
                return False
            else:
                if not res:
                    self.log('FAILED: %s %s' % (__fname__(), str(matches)))
                return res
        info = {
            'data': {'virt_id': virt_id, 'slot': slot, 'sys': sys, 'addr': addr},
            'device': None,
            'order': self.OP_RES_KO_SYS,
            'func': res_ko_sys
        }            
        return info

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
        info = {
            'data': {'slot': slot, 'sys': sys, 'addr': addr},
            'device': None,
            'order': self.OP_CMD_KO_SYS,
            'func': cmd_ko_sys
        }            
        return info

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
        info = {
            'data': {'virt_id': virt_id, 'slot': slot, 'index': index, 'value': value},
            'device': None,
            'order': self.OP_RES_PARAM_KO,
            'func': res_param_ko
        }            
        return info

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
        info = {
            'data': {'slot': slot, 'index': index, 'value': value},
            'device': None,
            'order': self.OP_CMD_PARAM_KO,
            'func': cmd_param_ko
        }            
        return info
