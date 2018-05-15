# -*- coding: utf-8 -*-

from .devices import Devices
from .basedevice import BaseDevice
from .bt_4652_2 import Device4652_2
from .bt_4652_3 import Device4652_3
from .bt_4693 import Device4693
from .bt_f411_2 import DeviceF411_2
from .bt_f411_4 import DeviceF411_4

# sorted by model_id
DeviceTypes = (
    Device4652_2,   # 2   - Automation basic control 2 buttons
    Device4652_3,   # 3   - Automation basic control 3 buttons
    Device4693,     # 21  - Basic temperature probe
    DeviceF411_2,   # 129 - 2 output relays
    DeviceF411_4,   # 130 - 4 output relays
)
