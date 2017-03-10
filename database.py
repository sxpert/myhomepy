#!/usr/bin/python

import sqlite3

class Database (object):

    def log (self, message):
        if self._log is not None:
            self._log (message)
        else:
            print (message)

    def __init__ (self, dbname, log=None):
        self._log = log
        self.conn = sqlite3.connect (dbname)
        c = self.conn.cursor()
        # check for presence of version table
        c.execute ("select count(*) from sqlite_master where name = 'version';")
        version_present = c.fetchone()[0]==1
        if not version_present:
            self.log ("[database/init] WARNING: Can't find the version table.")
            version = 0
        else:
            # read version 
            c.execute ("select version from version;")
            version_row = c.fetchone()
            self.log ("[database/init] info: version_row : "+str(version_row))
            if version_row is None:
                self.log ("[database/init] WARNING: Can't find version number, assume 0")
                version = 0
            else:
                version = version_row[0]
                self.log ("[database/init] info: Current version : "+str(version))

        if version == 0:
            # remove all tables
            self.log ("[database/init] info: remove all existing tables")
            c.execute ("select name from sqlite_master;")
            tables = c.fetchall()
            for t in tables:
                table = t[0]
                self.log ("[database/init] info: > "+table)
                c.execute (("drop table %s;"%table))
                
            # create version table
            self.log ("[database/init] info: create the version table")
            c.execute ("create table if not exists version (version integer);")
            self.log ("[database/init] info: >> COMMIT")
            self.conn.commit()

        # do stuff depending on current version
        if version == 0:
            # temperature log
            self.log ("[database/init] info: create temperatures table")
            c.execute ("create table if not exists temperatures ("+
                       "time integer,"+
                       "sensor integer,"+
                       "temp numeric,"
                       "primary key (time, sensor)) without rowid;")
            # update version to version 1
            self.log ("[database/init] info: set version to 1")
            c.execute ("insert into version (version) values (1);")
            self.log ("[database/init] info: >> COMMIT")
            self.conn.commit()
        else:
            self.log ("[database/init] info: Nothing to be done")

    def _execute (self, cursor, request, params):
        try:
            cursor.execute (request, params)
        except sqlite3.IntegrityError as e:
            return False
        except sqlite3.OperationalError as e:
            self.log ("[database/execute] ERROR [SQL] >> "+str(e))
            return None
        self.log ("[database/execute] SQL >> "+request+" "+str(params))
        return True
            

    def execute (self, request, params):
        c = self.conn.cursor()
        # execute contents of the queue
        try:
            queries = self._queries
        except AttributeError as e:
            queries = []
        ok = False
        while len(queries) > 0:
            s, v = queries[0]
            ok = self._execute (c, q, v)
            if ok is None:
                # something was broken
                # could not exec the last query, abort
                break
            # if either True or False, remove from list
            queries = queries[1:]

        if ok is None:
            # abort
            queries.append ((request, params,))
            self._queries = queries
            return None

        ok = self._execute (c, request, params)
        if ok is None:
            # push to queue
            queries.append((request, params,))
            self._queries = queries
            self.conn.rollback()
            return False
        if ok == False:
            self.conn.rollback()
        else:
            self.conn.commit()
        return ok

    # time is unix timestamp
    # sensor is sensor id
    # temp is in celcius
    def log_temperature (self, time, sensor, temp):
        self.execute ("insert into temperatures (time, sensor, temp) values (?,?,?);", (time, sensor, temp,))
