from .subsystem import OWNSubSystem
from .lighting import Lighting
from .temp_control import TempControl
from .gateway import Gateway
from .diag_lighting import DiagLighting
from .diag_temp_control import DiagTempControl
from .diag_gateway import DiagGateway


SubSystems = [Lighting,
              TempControl,
              Gateway,
              DiagLighting,
              DiagTempControl,
              DiagGateway, ]

# returns the appropriate class object
def find_subsystem(who):
    for s in SubSystems:
        if isinstance(who, int):
            if s.SYSTEM_WHO == who:
                return s
        if isinstance(who, str):
            if s.SYSTEM_NAME == who:
                return s
    return None
