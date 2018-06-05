# -*- coding: utf-8 -*-

from .devices import Devices
from .basedevice import BaseDevice
from .dev_bt_4652 import *
from .dev_bt_4693 import *
from .dev_bt_f411 import *

# sorted by model_id
DeviceTypes = (
    Device4652_2,   # 2   - Automation basic control 2 buttons
    Device4652_3,   # 3   - Automation basic control 3 buttons
    Device4693,     # 21  - Basic temperature probe
    DeviceF411_2,   # 129 - 2 output relays
    DeviceF411_4,   # 130 - 4 output relays
)
