import arrow
import database


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
    
    _timestamp = "{:d}".format(arrow.utcnow().timestamp)
    _sensor = "{:d}{:02d}".format(_zone, _sensor)
    _temp = "{:.1f}".format(_temp)
    system.log(
        "plugin: temperature/log_to_database (%s, %s, %s)" % 
        (str(_timestamp), str(_sensor), str(_temp)))
    return system.database.log_temperature(_timestamp, _sensor, _temp)
    