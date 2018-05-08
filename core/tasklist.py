# -*- coding: utf-8 -*-

import inspect
import threading


class TaskList(object):
    _parent = None
    _tasks = None
    _list_lock = None
    _stopped = None
    _stopped_indicator = None

    def __init__(self, parent=None):
        self._parent = parent
        self._tasks = []
        self._list_lock = threading.RLock()
        self._stopped = None
        self._stopped_indicator = None

    def log(self, msg):
        if self._parent is not None:
            self._parent.log(msg)
        else:
            print(msg)

    @property
    def has_task(self):
        if len(self._tasks) > 0:
            return True
        return False
    
    def __len__(self):
        return len(self._tasks)

    def push(self, task, wait=True, callback=None):

        class closure(object):
            __tasklist = self
            
            def __init__(self):
                tl = self.__tasklist
                tl.log('closure.__init__: task = %s' % (str(task)))
                if inspect.isclass(task):
                    if issubclass(task, threading.Thread):
                        tl.log('we have a subclass of thread')

                        class temp_subclass(task):
                            def run(self):
                                self.log('ts.run : must wait ? %s' % (str(wait)))
                                super().run()
                                self.log('ts.run : function has run it\'s course')
                                _tl = self.system.monitor._tasks
                                self.log('ts.run : %s' % (str(_tl)))
                                self.log('ts.run : %s' % (len(_tl)))
                                self.log('ts.run : callback ?')
                                if callback is not None:
                                    self.log('ts.run : callback ! %s' % (str(callback)))
                                    callback()
                                if wait:
                                    self.log('ts.run : locking the tasklist')
                                    _tl._list_lock.acquire()
                                    self.log('ts.run : setting stopped to false')
                                    _tl._stopped = False
                                    self.log('ts.run : unlocking the tasklist')
                                    _tl._list_lock.release()
                                self.log('ts.run : done')

                        tl.log('closure.__init__: wait ? %s' % (str(wait)))
                        if wait:
                            tl._list_lock.acquire()
                            tl._stopped = True
                            tl._list_lock.release()
                        func = temp_subclass(tl._parent)
                        tl._parent.system.main_loop.add_task(func)
                        tl.log('starting task %s' % (str(func)))
                        func.start()
                        return
                    else:
                        tl.log('not a thread')
                        return
                if inspect.isfunction(task):
                    tl.log('we have a bone headed function')
                    if wait:
                        tl._list_lock.acquire()
                        tl._stopped = True
                        tl._list_lock.release()
                    task(tl)
                    if callback:
                        callback()
                    if wait:
                        tl._list_lock.acquire()
                        tl._stopped = False
                        tl._list_lock.release()
        self._tasks.append(closure)

    def pop(self):
        if len(self._tasks) == 0:
            return None
        return self._tasks.pop(0)
    
    def execute_next(self):
        self._list_lock.acquire()
        if self._stopped:
            # print only once (should !)
            if not self._stopped_indicator:
                self.log('stopped!')
                self._stopped_indicator = True
            self._list_lock.release()
            return
        if self._stopped_indicator:
            self._stopped_indicator = False
        if not self.has_task:
            self._list_lock.release()
            return
        self.log('TaskList.execute_next: current list %s' % (str(self._tasks)))
        task = self.pop()
        self.log('TaskList: %s' % (str(self)))
        self.log('TaskList.execute_next: starting task %s' % (str(task)))
        task()
        self._list_lock.release()
