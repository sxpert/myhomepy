# -*- coding: utf-8 -*-
import datetime


from .subsystem import OWNSubSystem


class Gateway(OWNSubSystem):
    SYSTEM_WHO = 13

    SYSTEM_REGEXPS = {
        'STATUS': [
            (r'^\*\*#0\*(?P<hour>[0-2][0-9])\*(?P<minute>[0-5][0-9])\*(?P<second>[0-5][0-9])\*(?P<timezone>\d{1,3})##$', '_time_info', ),
            (r'^\*\*#1\*(?P<weekday>0[0-6])\*(?P<day>[0-3][0-9])\*(?P<month>[01][0-9])\*(?P<year>\d{4})##$', '_date_info', ),
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
        self.system.gateway.time_info(_time)
        return True
    
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
            self.log('weekday differs : got %d expected %d' % (_dow, _wd))
        self.system.gateway.date_info(_date)
        return True

    @staticmethod
    def gen_set_date_time(_dt):
        cmd = '*#13**#22*[hour]*[minute]*[second]*[tz]*[dow]*[day]*[month]*[year]##'
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
