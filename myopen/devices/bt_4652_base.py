# -*- coding: utf-8 -*-

from core.logger import *

from ..constants import *
from ..subsystems.lighting import Lighting
from .basedevice import BaseDevice
from .bt_4652_slot import Device4652_Slot


class Device4652_Base(BaseDevice):
    DEVICE_SYSTEM = Lighting
    SLOT_CLASS = Device4652_Slot

    def res_ko_value(self, virt_id, slot, keyo, state):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        return self.slots.res_ko_value(slot, keyo, state)

    def res_param_ko(self, virt_id, slot, index, val_par):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        return self.slots.res_param_ko(slot, index, val_par)
