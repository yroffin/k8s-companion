from threading import Lock, Thread

class Singleton(object):
    _instance = None
    _lock: Lock = Lock()

    def __new__(class_, *args, **kwargs):
        with Singleton._lock:
            if not isinstance(class_._instance, class_):
                class_._instance = object.__new__(class_, *args, **kwargs)
            return class_._instance
