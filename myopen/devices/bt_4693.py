# -*- coding: utf-8 -*-

from .basedevice import BaseDevice
from ..subsystems.temp_control import TempControl

class Device4693(BaseDevice):
    DEVICE_SYSTEM = TempControl.SYSTEM_WHO
    MODEL_ID = 21
    
