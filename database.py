#!/usr/bin/python

import sqlite3


class Database(object):

    def log(self, message):
        if self._log is not None:
            self._log(message)
        else:
            print(message)

    def __init__(self, dbname, log=None):
        self._log = log
        self.dbname = dbname
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        # check for presence of version table
        c.execute("select count(*) from sqlite_master where name = 'version';")
        version_present = c.fetchone()[0] == 1
        if not version_present:
            self.log("[database/init] WARNING: Can't find the version table.")
            version = 0
        else:
            # read version
            c.execute("select version from version;")
            version_row = c.fetchone()
            self.log("[database/init] info: version_row : "+str(version_row))
            if version_row is None:
                self.log("[database/init] WARNING: Can't find version number, "
                         "assume 0")
                version = 0
            else:
                version = version_row[0]
                self.log("[database/init] info: Current version : " +
                         str(version))

        if version == 0:
            # remove all tables
            self.log("[database/init] info: remove all existing tables")
            c.execute("select name from sqlite_master;")
            tables = c.fetchall()
            for t in tables:
                table = t[0]
                self.log("[database/init] info: > "+table)
                c.execute(("drop table %s;" % table))
            # create version table
            self.log("[database/init] info: create the version table")
            c.execute("create table if not exists version (version integer);")
            self.log("[database/init] info: >> COMMIT")
            conn.commit()

        # do stuff depending on current version
        if version == 0:
            # temperature log
            self.log("[database/init] info: create temperatures table")
            c.execute("create table if not exists temperatures ("
                      "time integer,"
                      "sensor integer,"
                      "temp numeric,"
                      "primary key (time, sensor)) without rowid;")
            # update version to version 1
            self.log("[database/init] info: set version to 1")
            c.execute("insert into version (version) values (1);")
            self.log("[database/init] info: >> COMMIT")
            conn.commit()
        else:
            self.log("[database/init] info: Nothing to be done")
        conn.close()

    def execute(self, cursor, request, params):
        try:
            cursor.execute(request, params)
        except sqlite3.IntegrityError as e:
            return False
        except sqlite3.OperationalError as e:
            self.log("[database/execute] ERROR [SQL] >> "+str(e))
            return None
        self.log("[database/execute] SQL >> "+request+" "+str(params))
        return True

    # --------------------------------------------------------------------------
    # temperatures

    # time is unix timestamp
    # sensor is sensor id
    # temp is in celcius
    def log_temperature(self, time, sensor, temp):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        res = self.execute(c,
                           "insert into temperatures (time, sensor, temp) "
                           "values (?,?,?);", (time, sensor, temp,))
        if res is bool and res:
            self.log("%d rows written" % (c.rowcount))
            conn.commit()
        conn.close()
        return res

    # lists all temperature sensors that logged something so far
    def list_temperature_sensors(self):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        sensors = c.execute("select distinct sensor from temperatures;")
        if sensors:
            sensors = []
            for r in c:
                sensors.append(r[0])
        conn.close()
        return sensors

    def read_temperatures(self, start, end, sensor):
        pass
