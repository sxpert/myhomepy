# -*- coding: utf-8 -*-

from .basedevice import BaseDevice
from ..subsystems.lighting import Lighting
from .bt_f411_slot import DeviceF411_Slot


class DeviceF411_Base(BaseDevice):
    DEVICE_SYSTEM = Lighting
    SLOT_CLASS = DeviceF411_Slot
