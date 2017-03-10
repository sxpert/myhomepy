import arrow
import database

def log_to_database (system, params, device, data):

    if "table" not in params:
        system.log ("ERROR: no \'table\' specified in params")
        return
    table = params["table"]
    if "zone" not in device:
        system.log ("ERROR: no \'zone\' specified in device")
        return
    zone = device["zone"]
    if "sensor" not in device:
        system.log ("ERROR: no \'sensor\' specified in device")
        return
    sensor = device["sensor"]
    if "temp" not in data:
        system.log ("ERROR: no \'temp\' specified in data")
        return
    temp = data["temp"]

    timestamp = "{:d}".format(arrow.utcnow().timestamp)
    sensor = "{:d}{:02d}".format(zone, sensor)
    temp = "{:.1f}".format(temp)
    system.log ("plugin: temperature/log_to_database ( "+timestamp+" "+sensor+" "+temp+" )")

    system.database.log_temperature(timestamp, sensor, temp)
    



