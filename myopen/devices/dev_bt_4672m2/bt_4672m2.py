# -*- coding: utf-8 -*-

from ...subsystems.lighting import Lighting
from ..basedevice import BaseDevice
from ..baseslot import BaseSlot


class Device4672M2(BaseDevice):
    DEVICE_SYSTEM = Lighting
    SLOT_CLASS = BaseSlot
    MODEL_ID = 82
