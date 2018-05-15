# -*- coding: utf-8 -*-
import datetime

from .subsystem import OWNSubSystem


class Gateway(OWNSubSystem):
    SYSTEM_WHO = 13

    OP_RES_TIME_INFO = 0
    OP_RES_DATE_INFO = 1

    SYSTEM_CALLBACKS = {
        'RES_TIME_INFO': OP_RES_TIME_INFO,
        'RES_DATE_INFO': OP_RES_DATE_INFO
    }

    SYSTEM_REGEXPS = {
        'STATUS': [
            (r'^\*\*#0\*(?P<hour>[0-2][0-9])\*(?P<minute>[0-5][0-9])'
             r'\*(?P<second>[0-5][0-9])\*(?P<timezone>\d{1,3})##$',
             '_time_info', ),
            (r'^\*\*#1\*(?P<weekday>0[0-6])\*(?P<day>[0-3][0-9])'
             r'\*(?P<month>[01][0-9])\*(?P<year>\d{4})##$',
             '_date_info', ),
        ]
    }

    def _time_info(self, matches):
        _hour = int(matches['hour'])
        _minute = int(matches['minute'])
        _second = int(matches['second'])
        _timezone = int(matches['timezone'])
        if _timezone >= 100:
            _timezone = -(_timezone - 100)
        _td = datetime.timedelta(hours=_timezone)
        _tz = datetime.timezone(_td)
        _time = datetime.time(_hour, _minute, _second, 0, _tz)
        res = self.system.gateway.time_info(_time)
        if not res:
            self.log('myopen.subsystems.Gateway._time_info WARNING : '
                     'time info not handled')
        _order = self.OP_RES_TIME_INFO
        _device = None
        _data = {'time': _time}
        return self.gen_callback_dict(_order, _device, _data)

    def _date_info(self, matches):
        _day = int(matches['day'])
        _month = int(matches['month'])
        _year = int(matches['year'])
        _dow = int(matches['weekday'])
        _date = datetime.date(_year, _month, _day)
        _wd = _date.isoweekday()
        if _wd == 7:
            _wd = 0
        # _dow should be == to _wd
        if _dow != _wd:
            # just log it, doesn't really matter, we don't use that info
            self.log('myopen.subsystems.Gateway._date_info WARNING : '
                     'weekday differs : got %d expected %d' % (_dow, _wd))
        res = self.system.gateway.date_info(_date)
        if not res:
            self.log('myopen.subsystems.Gateway._date_info WARNING : '
                     'date info not handled')
        _order = self.OP_RES_DATE_INFO
        _device = None
        _data = {'date': _date}
        return self.gen_callback_dict(_order, _device, _data)

    @staticmethod
    def gen_set_date_time(_dt):
        cmd = '*#13**#22*[hour]*[minute]*[second]*[tz]' \
              '*[dow]*[day]*[month]*[year]##'
        _tz = _dt.strftime('%z')
        _dow = _dt.isoweekday()
        params = {
            'year': '%04d' % (_dt.year),
            'month': '%02d' % (_dt.month),
            'day': '%02d' % (_dt.day),
            'dow': '%02d' % (0 if _dow == 7 else _dow),
            'hour': '%02d' % (_dt.hour),
            'minute': '%02d' % (_dt.minute),
            'second': '%02d' % (_dt.second),
            'tz': ('0' if _tz[0] == '+' else '1') + _tz[1:3]
        }
        from . import replace_in_command
        return replace_in_command(cmd, params)
