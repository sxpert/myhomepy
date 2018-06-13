# -*- coding: utf-8 -*-
from .asyncio_base_command import BaseCommand

from .asyncio_cmd_gateway_date_time import CmdGatewayUpdateDateTime
from .asyncio_cmd_general_off import CmdGeneralOff
#from .asyncio_base_command import *
from .asyncio_cmd_scan_aid import CmdScanAid
from .asyncio_cmd_diag_aid import CmdDiagAid

BUILT_IN_COMMANDS = (
    CmdGatewayUpdateDateTime,
    CmdGeneralOff,
    CmdScanAid,
    CmdDiagAid
) 
