# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagScannable(OWNSubSystem):
    SYSTEM_IS_SCANNABLE = True

    SCAN_REGEXPS = {
        'COMMAND': [
            # system is busy
            (r'^\*3\*0##$', '_diag_busy', ),
            
            # res_trans_end
            # end of transmission from device
            # *[who]*4*[_junk]##
            (r'^\*4\*(?P<_junk>.*)##$', '_diag_res_trans_end', ),
            
            # cmd_diag_abort
            # programmer abort diagnostic
            # *[who]*6*0##
            (r'^\*6\*0##$', '_diag_cmd_diag_abort', ),
            
            # cmd_diag_id
            # programmer starts a diagnostic session wth ID
            # *[who]*10#[id]*0##
            (r'^\*10#(?P<hw_addr>\d{1,10})\*0##$', '_diag_cmd_diag_id', ),
            # cmd_scan_check
            (r'^\*11#(?P<hw_addr>\d{1,10})\*0##$', '_cmd_scan_check', ),
            # scanning subsystem reset
            (r'^\*12\*0##$', '_subsystem_scan_reset', ),
            # 
        ],
        'STATUS': [
            # res_object_model
            # device answers with it's object model and number of physical configurators
            # *#[who]*[where]*1*[object_model]*[n_conf]*[brand]*[line]##
            (r'^\*(?P<virt_id>\d{1,4})\*1\*(?P<model_id>\d{1,3})\*(?P<nb_conf>\d{1,2})\*(?P<brand_id>\d)\*(?P<prod_line>\d)##$', '_diag_res_object_model', ),
            
            # res_fw_version
            # device answers with it's firmware version
            # *#[who]*[where]*2*[fw_version]##
            (r'^\*(?P<virt_id>\d{1,4})\*2\*(?P<fw_version>.*)##$', '_diag_res_fw_version', ),            
            
            # res_conf_1_6
            # device answers with hardware configurators 1 through 6
            # *#[who]*[where]*4*[c1]*[c2]*[c3]*[c4]*[c5]*[c6]##
            (r'^\*(?P<virt_id>\d{1,4})\*4\*(?P<c1>\d{1,2})\*(?P<c2>\d{1,2})\*(?P<c3>\d{1,2})\*(?P<c4>\d{1,2})\*(?P<c5>\d{1,2})\*(?P<c6>\d{1,2})##$', '_diag_res_conf_1_6', ),
            
            # res_diag_a
            # device answers with diagnostic bit set A
            # *#[who]*[where]*7*[bitmask_dia_a]##
            (r'^\*(?P<virt_id>\d{1,4})\*7\*(?P<diag_bits>[01]{24})##$', '_diag_res_diag_a', ),
            
            # device diagnostics
            # see notes.txt
            (r'^\*(?P<virt_id>\d{1,4})\*11\*(?P<diag_bits>[01]{24})##$', '_analyze_diagnostics', ),
            
            # res_id
            # device answers with it's ID
            # *#[who]*[where]*13*[id]##
            (r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$', '_diag_res_id', ),
            
            # res_ko_value
            # device answers with it's key/object, value and state
            # *#[who]*[where]*30*[slot]*[keyo]*[state]##
            (r'^\*(?P<virt_id>\d{1,4})\*30\*(?P<slot>\d{1,3})\*(?P<keyo>\d{1,3})\*(?P<state>\d{1,3})##$', '_diag_res_ko_value', ),
            
            # res_ko_sys
            # device answers with it's key/object, system and address",
            # *#[who]*[where]*32#[slot]*[sys]*[addr]##
            (r'^\*(?P<virt_id>\d{1,4})\*32#(?P<slot>\d{1,3})\*(?P<sys>\d{1,3})\*(?P<addr>\d{1,4})##$', '_diag_res_ko_sys', ),

            # res_param_ko
            # device answers with the key/value of key/object
            # *#[who]*[where]*35#[index]#[slot]*[val_par]##
            (r'\*(?P<virt_id>\d{1,4})\*35#(?P<index>\d{1,3})#(?P<slot>\d{1,3})\*(?P<val_par>\d{1,10})##', '_diag_res_param_ko', ),
        ]
    }

    def parse_regexp(self, msg):
        sys_regexps = self.get_regexps(msg, 'SYSTEM_REGEXPS')
        scan_regexps = self.get_regexps(msg, 'SCAN_REGEXPS')
        regexps = sys_regexps + scan_regexps
        return self._parse_regexp(msg, regexps)

    def _diag_busy(self, matches):
        return True

    def _diag_res_trans_end(self, matches):
        self.log('res_trans_end %s' % (str(matches)))
        return self.system.devices.eot_event(self, matches)

    def _diag_cmd_diag_abort(self, matches):
        self.log('cmd_diag_abort %s' % (str(matches)))
        return True

    def _diag_cmd_diag_id(self, matches):
        _hw_addr = int(matches.get('hw_addr', None))
        return self.system.devices.set_active_device(self, _hw_addr)

    def _cmd_scan_check(self, matches):
        return True

    def _subsystem_scan_reset(self, matches):
        # self.log('scan reset for %d subsystem' % self.SYSTEM_WHO)
        return True

    def _diag_res_object_model(self, matches):
        self.log('res_object_model %s' % (str(matches)))
        return True

    def _diag_res_fw_version(self, matches):
        self.log('res_fw_version %s' % (str(matches)))
        return True

    def _diag_res_conf_1_6(self, matches):
        self.log('res_conf_1_6 %s' % (str(matches)))
        return True

    def _diag_res_diag_a(self, matches):
        self.log('res_diag_a %s' % (str(matches)))
        return True

    def _analyze_diagnostics(self, matches):
        self.log('DiagScannable dev diags : %s' % str(matches))
        return True

    def _diag_res_id(self, matches):
        self.log('res_id %s' % str(matches))
        self.system.devices.register(self, matches)
        return True
    
    def _diag_res_ko_value(self, matches):
        self.log('res_ko_value %s' % (str(matches)))
        return True

    def _diag_res_ko_sys(self, matches):
        self.log('res_ko_sys %s' % (str(matches)))
        return True

    def _diag_res_param_ko(self, matches):
        self.log('res_param_ko %s' % (str(matches)))
        return True
