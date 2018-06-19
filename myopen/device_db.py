import sqlite3
from core.logger import get_logger, COLOR_LT_MAGENTA


class DeviceDatabase(object):

    def __init__ (self):
        self.log = get_logger(header='[DEVS]', color=COLOR_LT_MAGENTA)
        self.log("Initializing device database")
        # TODO: better path handling
        self.conn = sqlite3.connect("device_catalog.db")

    # ------------------------------------------------------------------------
    #
    # utilities
    #
    #

    def match_fw(self, dev_firmware, to_check):
        if dev_firmware is None:
            return False
        dev_firmware = dev_firmware.split('.')
        to_check = to_check.split('.')
        if len(dev_firmware) != 3:
            self.log("error, device firmware should have 3 components")
            return False
        if len(to_check) != 3:
            self.log("error, firmware to check should have 3 components")
            return False
        ok = True
        for n in range(0, len(to_check)):
            tc = to_check[n]
            fw = dev_firmware[n]
            if tc == '*':
                continue
            if tc != fw:
                ok = False
        return ok

    # ------------------------------------------------------------------------
    #
    # Value checking utilities
    #
    #

    def check_ok(self, value):
        return (True, value,)

    def check_error(self, message):
        self.log(message)
        return (False, None,)

    def check_ADDRESS_lighting(self, addr):
        if addr is None:
            return self.check_error("ERROR: address can't be None")
        if 'a' not in addr.keys():
            return self.check_error("ERROR: invalid address, missing a")
        if 'pl' not in addr.keys():
            return self.check_error("ERROR: invalid address, missing pl")
        a = addr.get('a', None)
        pl = addr.get('pl', None)
        if a is None:
            return self.check_error("ERROR: invalid address, a is None")
        if pl is None:
            return self.check_error("ERROR: invalid address, pl is None")
        if a == 0 and pl == 0:
            return self.check_error("ERROR: invalid address, a:0/pl:0 is not acceptable")
        if a < 0 or a > 10:
            return self.check_error("ERROR: invalid address, a(%d) should be in [0..10]" % a)
        if pl <0 or pl > 15:
            return self.check_error("ERROR: invalid address, pl(%d) should be in [0..15]" % pl)
        return self.check_ok(addr)

    def check_ADDRESS_slave_probe(self, addr):
        if addr is None:
            return self.check_error("ERROR: address can't be None")
        if 'zone' not in addr.keys():
            return self.check_error("ERROR: invalid address, missing zone")
        if 'slave' not in addr.keys():
            return self.check_error("ERROR: invalid address, missing slave")
        zone = addr.get('zone', None)
        slave = addr.get('slave', None)
        if 'zone' not in addr.keys():
            return self.check_error("ERROR: invalid address, zone is None")
        if 'slave' not in addr.keys():
            return self.check_error("ERROR: invalid address, slave is None")
        if zone < 1 or zone > 99:
            return self.check_error("ERROR: invalid address, zone(%d) should be in [1..99]" % zone)
        if slave < 1 or slave > 9:
            return self.check_error("ERROR: invalid address, slave(%d) should be in [0..9]" % slave)
        return self.check_ok(addr)

    # ------------------------------------------------------------------------
    #
    # Parsing and value checking utilities
    #
    #

    def parse_ADDRESS_8_bit(self, value):
        if isinstance(value, str):
            value = int(value)
        if isinstance(value, int):
            a = (value & 0xf0) >> 4
            pl = value & 0xf
            addr = {'a': a, 'pl': pl}
        elif isinstance(value, dict):
            addr = value
        elif value is None:
            self.log("parse_ADDRESS_8_bit WARNING: value is None")
            addr = value
        else: 
            return self.check_error("parse_ADDRESS_8_bit ERROR: unknown value %s %s" % (value.__class__.__name__, str(value)))
        return self.check_ADDRESS_lighting(addr)

    def parse_ADDRESS_long(self, value):
        if isinstance(value, str):
            a = None
            pl = None
            if len(value) == 2:
                a = int(value[0])
                pl = int(value[1])
            elif len(value) == 4:
                a = int(value[0:2])
                pl = int(value[2:4])
            addr = {'a': a, 'pl': pl}
        elif isinstance(value, dict):
            addr = value
        elif value is None:
            self.log("parse_ADDRESS_long WARNING: value is None")
            addr = value
        else: 
            return self.check_error("parse_ADDRESS_long ERROR: unknown value %s %s" % (value.__class__.__name__, str(value)))
        return self.check_ADDRESS_lighting(addr)

    def parse_ADDRESS_slave_probe(self, value):
        if isinstance(value, str):
            zone = None
            slave = None
            if len(value) == 3:
                slave = int(value[0])
                zone = int(value[1:3])
            addr = {'zone': zone, 'slave': slave}
        elif isinstance(value, dict):
            addr = value
        elif value is None:
            self.log("parse_ADDRESS_slave_probe WARNING: value is None")
            addr = value
        else: 
            return self.check_error("parse_ADDRESS_slave_probe ERROR: unknown value %s %s" % (value.__class__.__name__, str(value)))
        return self.check_ADDRESS_slave_probe(addr)

    def parse_BOOL(self, field_type_detail, value):
        if isinstance(value, int):
            if value not in (0, 1):
                self.log("WARNING: bool value (%d) should be either (0, False) or (1, True)" % value)
            value = value != 0
        if not isinstance(value, bool):
            self.log("ERROR: value should be a bool type at this point")
            return self.check_error(value)
        return self.check_ok(value)

    def parse_INTEGER(self, field_type_detail, value):
        # TODO: handle array value
        if isinstance(value, int):
            c = self.conn.cursor()
            sql = "select value_undef, value_min, value_max from integers where type=?"
            c.execute(sql, [field_type_detail])
            vals = c.fetchall()
            if len(vals) == 0:
                return self.check_error("ERROR: unable to find definition for integer %s" % field_type_detail)
            # at this point we must have one record
            v_undef, v_min, v_max = vals[0]
            self.log('DeviceDatabase.parse_INTEGER : field_type_detail: %s value %s undef: %s min: %s max: %s' % 
                (str(field_type_detail), str(value), str(v_undef), str(v_min), str(v_max)))
            if value != v_undef:
                if value < v_min or value > v_max:
                    return self.check_error("ERROR: invalid value %d for integer %s, should be in [%d..%d]" %
                                            (value, field_type_detail, v_min, v_max))
            else:
                value = None
        else:
            return self.check_error("parse_INTEGER ERROR: %s expected an int value (%s)" % (field_type_detail, str(value)))
        self.log('DeviceDatabase.parse_INTEGER : integer ok %d' % (value))
        return self.check_ok(value)

    def parse_LIST(self, field_type_detail, value):
        c = self.conn.cursor()
        if isinstance(value, int):
            # check int value
            pass
        elif isinstance(value, str):
            sql = "select value from lists where list_ref=? and id=?;"
            c.execute(sql, [field_type_detail, value])
            val = c.fetchall()
            if len(val) == 0:
                # try the old_id
                sql = "select value from lists where list_ref=? and old_id=?;"
                c.execute(sql, [field_type_detail, value])
                val = c.fetchall()
            if len(val) != 1:
                return self.check_error("parse_LIST %s %s ERROR, should have exactly one record here %s" % 
                                        (field_type_detail, value, str(val)))
            value = val[0][0]
        return self.check_ok(value)

    def parse_value(self, value, field_type, field_type_detail):
        self.log('DeviceDatabase.parse_value value: %s field_type: %s field_type_detail: %s' %
            (str(value), str(field_type), str(field_type_detail)))
        f_name = "parse_%s" % (field_type)
        func = getattr(self, f_name, None)
        if func is not None:
            return func(field_type_detail, value)
        f_name = "parse_%s_%s" % (field_type, field_type_detail)
        func = getattr(self, f_name, None)
        if func is not None:
            return func(value)
        return self.check_error("unable to find parser for %s.%s" % (field_type, field_type_detail))

    # ------------------------------------------------------------------------
    #
    # value exporting utilities
    #
    #

    def export_LIST(self, field_type_detail, value):
        c = self.conn.cursor()
        sql = "select id from lists where list_ref=? and value=?;"
        try:
            c.execute(sql, [field_type_detail, value])
        except Exception as e:
            # TODO: handle the array case !
            return self.check_error("DeviceDatabase.export_LIST ERROR: ['%s', '%s'] <%s>" % (str(field_type_detail), str(value), str(e)))
        val = c.fetchall()
        if len(val) != 1:
            return self.check_error("export_LIST: should have only one record here")
        return self.check_ok(val[0][0])

    def export_value(self, value, field_type, field_type_detail):
        f_name = "export_%s" % field_type
        func = getattr(self, f_name, None)
        if func is not None:
            return func(field_type_detail, value)
        # if we can't find a function for this, just return the value
        return self.check_ok(value)

    # ------------------------------------------------------------------------
    #
    # Database searching functions
    #
    #

    def get_ko_details(self, ko_value):
        """
        Gets details for a ko

        returns a tuple with
        - slot width
        - label
        - description
        """
        c = self.conn.cursor()
        sql = 'select slot_width, label, description from kos where ko=?;'
        c.execute(sql, [ko_value])
        ko_data = c.fetchall()
        if len(ko_data) != 1:
            self.log("get_ko_details ERROR: exactly 1 record expected")
            return None
        return ko_data[0]

    def cast_value(self, field_type, default):
        if default is None: return default
        if field_type=='BOOL': 
            if default is None: return False
            if default.lower() in ('true', 't', '1',): return True
            if default.lower() in ('false', 'f', '0',): return False
            return False
        if field_type=='TEMP':
            return float(default)
        # catch all...
        return default

    def get_params_for_ko(self, ko_value):
        """
        """
        c = self.conn.cursor()
        sql = 'select "order", cond, disp, access, type, type_info, def_val, tab, ' \
              'var_name, array_index, description from ko_params ' \
              'where ko=? order by "order";'
        c.execute(sql, [ko_value])
        params = c.fetchall()
        data = []
        for p in params:
            order, cond, disp, access, field_type, field_type_detail, def_val, tab, var_name, array_index, description = p
            val = {}
            val['order'] = order
            val['cond'] = cond
            val['disp'] = disp=='true'
            val['access'] = access
            val['field_type'] = field_type
            val['field_type_detail'] = field_type_detail
            val['default_value'] = self.cast_value(field_type, def_val)
            val['tab'] = tab
            val['var_name'] = var_name
            val['array_index'] = array_index
            val['description'] = description
            data.append(val)
        return data

    def get_condition_details(self, cond):
        c = self.conn.cursor()
        sql = 'select op, type, field, value, cond1, cond2 from cond where cond=?'
        conds_id = [cond]
        conds = {}
        while len(conds_id) > 0:
            cond = conds_id.pop(0)
            c.execute(sql, [cond])
            cond_info = c.fetchall()
            if len(cond_info) != 1:
                self.log('get_condition_details ERROR: expected only one record')
            try:
                op, field_type, field_name, value, cond1, cond2 = cond_info[0]
            except IndexError:
                self.log('erh, wtf happened here ? %s %s' % (str(cond), str(cond_info)))
            else:
                data = {}
                data['op'] = op
                data['field_type'] = field_type
                data['field_name'] = field_name
                data['value'] = value
                data['cond1'] = cond1
                if cond1 is not None:
                    conds_id.append(cond1)
                data['cond2'] = cond2
                if cond2 is not None:
                    conds_id.append(cond2)
                conds[cond] = data
        return conds

    def get_integer_details(self, integer_name):
        c = self.conn.cursor()
        sql = 'select value_min, value_max from integers where type=?;'
        c.execute(sql, [integer_name])
        val = c.fetchall()
        if len(val) != 1:
            self.log('get_integer_details ERROR: expected only 1 record (%s) \'%s\'' % (str(integer_name), str(val)))
            return None
        val_min, val_max = val[0]
        data = {}
        data['min'] = val_min
        data['max'] = val_max
        return data

    def get_list_details(self, list_ref):
        c = self.conn.cursor()
        sql = 'select value, id, name from lists where list_ref=? order by "order";'
        c.execute(sql, [list_ref])
        values = []
        ids = []
        names = []
        val = c.fetchall()
        for v in val:
            value, id, name = v
            values.append(value)
            ids.append(id)
            names.append(name)
        data = {}
        data['values'] = values
        data['ids'] = ids
        data['names'] = names
        return data

    def find_kos_for_device(self, system_id, model_id, firmware, slot_number):
        """
        List KOs available for device with firmware
        """
        kos = []
        c = self.conn.cursor()
        # list all kos valid for slot
        sql = "select fw, tab_label, ko from device_kos where system_id=? and model_id=? and slot=? order by \"order\";"
        c.execute(sql, [system_id, model_id, slot_number])
        ko_entries = c.fetchall()
        for entry in ko_entries:
            fw, tab_label, ko = entry
            if self.match_fw(firmware, fw):
                kos.append((ko, tab_label,))
        return kos

    def find_symbolic_kos_for_device(self, system_id, model_id, firmware, slot_number):
        kos = self.find_kos_for_device(system_id, model_id, firmware, slot_number)
        c = self.conn.cursor()
        data = {}
        sql = "select label, slot_width from kos where ko=?;"
        for ko_rec in kos:
            ko, _ = ko_rec
            c.execute(sql, [ko])
            label = c.fetchall()
            if len(label) != 1:
                self.log("find_symbolic_kos_for_device ERROR: should only have one record")
                raise AssertionError
            label, width = label[0]
            if width is None: 
                width = 1
            data[label] = (ko, width,)
        return data

    def find_symbolic_ko_value(self, ko):
        c = self.conn.cursor()
        sql = "select label from kos where ko=?;"
        c.execute(sql, [ko])
        val = c.fetchall()
        if len(val) != 1:
            self.log("find_symbolic_ko_value ERROR: should only have one record")
            value = ko
        else:
            value = val[0][0]
        return value

    def find_fields_for_ko(self, ko):
        c = self.conn.cursor()
        sql = "select distinct var_name, var_old from ko_params where ko=? order by \"order\";"
        c.execute(sql, [ko])
        fields = c.fetchall()
        return fields

    def find_sys_addr(self, ko):
        """
        Find the ADDR record for the KO

        returns a tuple with
        - order
        - slot_param
        - type_info
        - var_name
        - description
        """
        if ko is None:
            self.log("find_sys_addr ERROR: ko can't be None")
        c = self.conn.cursor()
        sql = "select \"order\", slot_param, access, type, type_info, var_name, description " \
              "from ko_params where ko=? and slot_param='ADDR';"
        c.execute(sql, [ko])
        rec = c.fetchall()
        if len(rec) > 1:
            self.log("find_sys_addr ERROR: I should have obtained only one record")
            return None
        if len(rec) == 0:
            self.log("find_sys_addr ERROR: I should have found something !")
            return None
        return rec[0]

    def get_field_value(self, f_type, field, val_id):
        c = self.conn.cursor()
        vals = None
        if f_type == 'LIST':
            sql = "select value from lists where list_ref=? and id=?;"
            c.execute(sql, [field, val_id])
            vals = c.fetchall()
            if len(vals) == 1:
                return vals[0][0]
        self.log("get_field_value ERROR: bad number of records returned for %s[%s.%s] => %s" % (f_type, field, val_id, str(vals)))

    def recurse_conditions(self, cond, get_value):
        c = self.conn.cursor()
        sql = "select * from cond where cond=?;"
        c.execute(sql, [cond])
        cond_rec = c.fetchall()
        if len(cond_rec) == 0:
            self.log("recurse_conditions ERROR: unable to find cond %s" % (cond))
            return False
        if len(cond_rec) > 1:
            self.log("recurse_conditions ERROR: got more than one record for cond %s" % (cond))
            return False
        _, op, f_type, field, value, cond1, cond2 = cond_rec[0]
        if op == "==":
            v = self.get_field_value(f_type, field, value)
            cv = get_value(field, None)
            if cv is None:
                self.log("recurse_conditions ERROR: unable to retrieve value for %s in op %s" % (field, op))
                return False
            return v==cv
        elif op == "OR":
            c1 = self.recurse_conditions(cond1, get_value)
            c2 = self.recurse_conditions(cond2, get_value)
            return c1 or c2
        else:
            self.log("recurse_conditions ERROR: unknown op '%s' in cond %s" % (op, cond))
            return False


    def find_field(self, ko, index, get_value):
        """
        finds the corresponding field for index using values already in the slot
        
        returns either None or a tuple with ...
        - access_mode
        - field_type
        - field_type_detail
        - var_name
        - array_index
        """
        c = self.conn.cursor()
        sql = "select cond, access, type, type_info, var_name, array_index "\
              " from ko_params where ko=? and param_id=?;"
        c.execute(sql, [ko, index])
        recs = c.fetchall()
        vr = []
        for r in recs:
            cond = r[0]
            if cond is not None:
                if self.recurse_conditions(cond, get_value):
                    vr.append(r)
            else:
                vr.append(r)
        # vr should contain 0 or 1 record...
        if len(vr) > 1:
            self.log("find_field ERROR: there should be 0 or 1 record %s" % (str(vr)))
        if len(vr) == 1:
            _, access, f_type, type_info, var_name, array_index = vr[0]
            return (access, f_type, type_info, var_name, array_index,)
        return None

    def find_named_field(self, ko, field_name, get_value):
        """
        finds the corresponding field for field_name using values already in the slot
        
        returns either None or a tuple with ...
        - access_mode
        - field_type
        - field_type_detail
        """
        c = self.conn.cursor()
        sql = "select distinct cond, access, type, type_info"\
              " from ko_params where ko=? and var_name=? and disp='true';"
        c.execute(sql, [ko, field_name])
        recs = c.fetchall()
        vr = []
        for r in recs:
            cond = r[0]
            if cond is not None:
                if self.recurse_conditions(cond, get_value):
                    vr.append(r)
            else:
                vr.append(r)
        # vr should contain 0 or 1 record...
        if len(vr) > 1:
            self.log("find_named_field ERROR: there should be 0 or 1 record %s" % (str(vr)))
        if len(vr) == 1:
            _, access, f_type, type_info = vr[0]
            return (access, f_type, type_info)
        return None
    

device_db = DeviceDatabase()