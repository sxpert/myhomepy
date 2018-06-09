# -*- coding: utf-8 -*-
from ..baseslot import BaseSlot

class Device4652_Slot(BaseSlot):
    
    @property
    def slot_options(self):
        options = super().slot_options
        options['slot_type']= '4652'
        return options
