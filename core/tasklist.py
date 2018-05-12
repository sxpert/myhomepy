# -*- coding: utf-8 -*-

import inspect
import threading
import types


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

    def push(self, task, wait=True, callback=None, params=None):

        class closure(object):
            __tasklist = self
            __func = None
            
            def __init__(self):
                tl = self.__tasklist
                tl.log('closure.__init__: task = %s' % (str(task)))
                if inspect.isclass(task):
                    if issubclass(task, threading.Thread):

                        if wait:
                            tl._list_lock.acquire()
                            tl._stopped = True
                            tl._list_lock.release()

                        self.__func = task(tl._parent)

                        old_run = getattr(self.__func, 'run')
                        
                        cb = None
                        if callback is not None:
                            cb = types.MethodType(callback, self.__func)
                        
                        def run(*args, **kwargs):
                            # the run function only takes one parameter
                            if len(args) != 1:
                                # should never happen
                                raise TypeError('run(self) missing 1 required positional argument: \'self\'')
                            _self = args[0]
                            if params is not None:
                                old_run(params)
                            else:
                                old_run()
                            # run callback if available
                            if cb is not None:
                                cb()
                            if wait:
                                tl._list_lock.acquire()
                                tl._stopped = False
                                tl._list_lock.release()

                        setattr(self.__func, 'run', types.MethodType(run, self.__func))

                        tl._parent.system.main_loop.add_task(self.__func)
                        self.__func.start()
                        return
                        
                    else:
                        tl.log('not a thread')
                        return
                if inspect.isfunction(task):
                    # TODO: this needs to be tested some more
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
        return closure

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
        task = self.pop()
        task()
        self._list_lock.release()
