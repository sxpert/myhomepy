# -*- coding: utf-8 -*-
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
        self.log('Gateway._time_info %s' % (str(matches)))
        return True
    
    def _date_info(self, matches):
        self.log('Gateway._date_info %s' % (str(matches)))
        return True