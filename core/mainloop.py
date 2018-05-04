# -*- coding: utf-8 -*-

import time
import sys

# --------------------------------------------------------------------------------------------------
#
# System main loop, handles events
#


class MainLoop(object):
    """
    main program loop
    manages threads
    """
    def __init__(self, logger, timeout=0.2):
        self.tasks = []
        self.timers = []
        self.stopped = False
        self.logger = logger
        self.timeout = timeout

    def log(self, msg):
        col_in = '\033[91m'
        col_out = '\033[0m'
        self.logger.log('[LOOP] ' + col_in + msg + col_out)

    def add_task(self, task):
        self.log("adding task "+str(task))
        self.tasks.append(task)

    def wait_all(self):
        """
        stops all registered tasks,
        then joins them
        """
        for task in self.tasks:
            self.logger.log("waiting on server "+str(task))
            task.stop()
            try:
                task.join()
            except KeyboardInterrupt:
                pass
        self.log(str("all remaining servers stopped"))

    def run(self):
        """
        main program loop.
        handles keyboard interrupt, stops all other threads in that case
        """
        # start all registered tasks
        for task in self.tasks:
            # try starting the task
            try:
                task.start()
            except RuntimeError:
                # hah, task already started, ignore
                pass
        try:
            self.log("running main loop")
            while not self.stopped:
                time.sleep(1)
                # cleanup dead threads
                tasklist = []
                changed = False
                for t in self.tasks:
                    try:
                        t.start()
                    except RuntimeError:
                        # thread already started, we're fine
                        pass
                    if not t.is_alive():
                        self.log("task %s is dead" % (str(t)))
                        t.join(0.1)
                        changed = True
                    else:
                        tasklist.append(t)
                if changed:
                    # self.log("task list %s" % (str(tasklist)))
                    self.tasks = tasklist
        except KeyboardInterrupt:
            self.log("^C forcing program exit")
            self.wait_all()
            sys.exit(0)
