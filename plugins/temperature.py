from datetime import datetime, timezone
import database
from core.logger import *


def log_to_database(system, params, device, data):
    # ignore the table stuff for now, will need be done though

    # if "table" not in params:
    #     system.log("ERROR: no \'table\' specified in params")
    #     return
    # table = params["table"]
    _zone = device.get('zone', None)
    if not _zone:
        system.log("ERROR: no \'zone\' specified in device")
        return
    _sensor = device.get('sensor', None)
    if not _sensor:
        system.log("ERROR: no \'sensor\' specified in device")
        return
    _temp = data.get('temp', None)
    if not _temp:
        system.log("ERROR: no \'temp\' specified in data")
        return

    _ts_int = int(datetime.now(timezone.utc).timestamp())
    _timestamp = "{:d}".format(_ts_int)
    _sensor = "{:d}{:02d}".format(_zone, _sensor)
    _temp = "{:.1f}".format(_temp)
    # not a warning
    system.log("plugins.temperature.log_to_database (%s, %s, %s)" %
               (str(_timestamp), str(_sensor), str(_temp)), LOG_INFO)
    _db = system.database
    if _db is not None:
        return _db.log_temperature(_timestamp, _sensor, _temp)
    system.log('plugins.temperature.log_to_database WARNING : no database')
    return None
