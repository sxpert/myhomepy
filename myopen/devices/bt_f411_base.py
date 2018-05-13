# -*- coding: utf-8 -*-

from .basedevice import BaseDevice
from ..subsystems.lighting import Lighting

class DeviceF411_Base(BaseDevice):
    DEVICE_SYSTEM = Lighting.SYSTEM_WHO
    pass
    
