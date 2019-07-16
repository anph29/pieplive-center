import threading


def timeout(fn, sec):
    timeout = threading.Timer(sec, fn)
    timeout.start()
    return timeout


# def clear_timeout(timeout):
#     timeout.cancel()


def interval(fn, sec):
    def func_wrapper():
        interval(fn, sec)
        fn()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


# def clear_interval(interval):
#     interval.cancel()
