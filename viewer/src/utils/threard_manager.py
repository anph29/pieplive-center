from threading import Thread
import time


class Manager(object):
    callback = None

    def __init__(self, cb=None):
        self.callback = cb

    def new_thread(self, need_running):
        return PiepThread(parent=self, cb=need_running)

    def on_thread_finished(self, thread, data):
        self.callback and self.callback(data)


class PiepThread(Thread):
    callback = None

    def __init__(self, parent=None, cb=None):
        self.parent = parent
        self.callback = cb
        super(PiepThread, self).__init__()

    def run(self):
        self.callback and self.callback()
        self.parent and self.parent.on_thread_finished(self, "Anph")

    def is_running(self):
        return self.isAlive()

    def shut_down(self):
        # block while waiting for thread to terminate
        while self.isAlive():
            time.sleep(1)
            return True


if __name__ == "__main__":

    def anph(dt):
        print(dt, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def anph1(dt):
        print(dt, "aaaaaaaaaaaaaaaaaaa2222222222222aaaaaaaaaaaaaaaaaaaa")

    mgr = Manager()
    thread = mgr.new_thread(anph1)
    thread.start()
