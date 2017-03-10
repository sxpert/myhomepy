#!/usr/bin/python

import database
import re
import json
import time
import arrow
import datetime 
import dateutil

def generate_database ():
    # read system timezone
    tzfile = open("/etc/timezone","r")
    tz_name = tzfile.readline()
    tzfile.close()
    if tz_name[-1]=="\n":
        tz_name=tz_name[0:-1]

    db = database.Database("grenoble.db")
    log = open("myopenlog-2.log")
    lines = 0
    temps = 0
    last_str = ""
    last = None
    json_re = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\ "+
                         "(?P<time>\d{2}:\d{2}:\d{2})\ "+
                         "\[(?P<host>[^:]+):(?P<port>\d+)\ "+
                         "(?P<sock_mode>[^\]]+)\]"+
                         "[^\{]*(?P<json>\{.*\})")
    while True:
        l = log.readline()
        if l == "":
            break
        lines+=1
        m = json_re.match (l) 
        if m is not None:
            g = m.groupdict()
            ok = False
            try:
                js = json.loads(g['json'])
            except ValueError as e:
                # not json format, could be a string version of a python dict
                try:
                    js = eval(g['json'])
                except SyntaxError as e:
                    pass
                except TypeError as e:
                    pass
                else:
                    ok = True
            else: 
                ok = True
            if ok and type(js) is dict:
                if "temperature" in js.keys():
                    temps+=1
                    js["time"] = g["time"]
                    js["date"] = g["date"]
                    # generate unix timestamp
                    dt = arrow.get(datetime.datetime.strptime(js["date"]+" "+js["time"],"%Y-%m-%d %H:%M:%S"), dateutil.tz.gettz(tz_name))
                    js["timestamp"] = dt.timestamp
                    t = js["temperature"]
                    temp = float(t[1:])/10
                    if t[0]=="1":
                        temp=-temp
                    js["temperature"] = temp

                    if db.log_temperature(js["timestamp"], js["probe"], js["temperature"]):
                        print json.dumps(js)

                    

    print str(lines)+" lines read"
    print str(temps)+" temperatures read"

if __name__ == "__main__":
    generate_database()
