# -*- coding: utf-8 -*-

from ...subsystems.temp_control import TempControl
from ..basedevice import BaseDevice
from .bt_4693_slot import Device4693_Slot


class Device4693(BaseDevice):
    DEVICE_SYSTEM = TempControl
    MODEL_ID = 21
    SLOT_CLASS = Device4693_Slot
