from .subsystem import OWNSubSystem
from .lighting import Lighting
from .temp_control import TempControl
from .gateway import Gateway
from .diag_scannable import DiagScannable
from .diag_lighting import DiagLighting
from .diag_temp_control import DiagTempControl
from .diag_gateway import DiagGateway


SubSystems = [Lighting,
              TempControl,
              Gateway,
              DiagLighting,
              DiagTempControl,
              DiagGateway, ]

TX_CMD_SCAN_SYSTEM = "*#[who]*0*13##"
TX_CMD_DIAG_ABORT = "*[who]*6*0##"
TX_CMD_DIAG_ID = "*[who]*10#[id]*0##"
TX_CMD_SCAN_CHECK = "*[who]*11#[id]*0##"
TX_CMD_RESET = "*[who]*12*0##"
TX_CMD_PARAM_ALL_KO = "*#[who]*0*38#0##"

# returns the appropriate class object
def find_subsystem(who):
    for s in SubSystems:
        if isinstance(who, int):
            if getattr(s, 'SYSTEM_WHO', None) == who:
                return s
        if isinstance(who, str):
            if getattr(s, 'SYSTEM_NAME', 'UNKNOWN') == who:
                return s
    return None

def find_scannable():
    _scan = []
    for s in SubSystems:
        if getattr(s, 'SYSTEM_IS_SCANNABLE', False):
            _scan.append(s)
    return _scan

def replace_in_command(command, params):
    _cmd = ''
    _in_var = False
    _var = ''
    for c in command:
        if _in_var:
            if c == ']':
                # replace var
                if _var in params.keys():
                    _cmd += str(params[_var])
                _in_var = False
                _var = ''
            else:
                _var += c
            continue
        if c == '[':
            _in_var = True
            continue
        _cmd += c
    return _cmd
