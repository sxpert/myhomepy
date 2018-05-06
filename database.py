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
            if version_row is None:
                self.log("[database/init] WARNING: Can't find version number, "
                         "assume 0")
                version = 0
            else:
                version = version_row[0]
            
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

    def _sql_log_error(self, error, data):
        self.log("Error executing request %s" % (str(data)))
        self.log(error)
        return False

    def _do_insert(self, table, fields, values):
        # create request
        if len(fields) != len(values):
            self.log("ERROR, fields %s and values %s numbers mismatch" %
                     (fields, values))
            return False
        _fields = '(%s)' % (', '.join(fields))
        _placeholders = '(%s)'% (', '.join(['?'] * len(values)))
        _request = "insert into %s %s values %s;" % (
            table, _fields, _placeholders
        )
        # open connection
        conn = sqlite3.connect(self.dbname)
        # execute request
        c = conn.cursor()
        try:
            c.execute(_request, values)
        except sqlite3.IntegrityError as e:
            return self._sql_log_error(e, (_request, values,))
        except sqlite3.OperationalError as e:
            return self._sql_log_error(e, (_request, values,))
        # verify if all is ok - only one row here
        _rc = c.rowcount
        if _rc != 1:
            return self._sql_log_error(
                "wrong rowcount after insert, expected 1, got %d" % (_rc),
                (_request, values,))
        self.log("request successful %s rows: %d" 
                 % (str((_request, values,)), _rc))
        # commit
        conn.commit()
        # close connection
        conn.close()
        # return result
        return True

    # --------------------------------------------------------------------------
    # temperatures

    # time is unix timestamp
    # sensor is sensor id
    # temp is in celcius
    def log_temperature(self, time, sensor, temp):
        return self._do_insert('temperatures', 
                               ['time', 'sensor', 'temp'], 
                               [time, sensor, temp])

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
