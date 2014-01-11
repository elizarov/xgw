from threading import Thread
import sys

class Worker(Thread):
    def __init__(self, **args):
        Thread.__init__(self, **args)
        self._closed = False

    def close(self):
        self._closed = True
        self.join()

    def run(self):
        while not self._closed:
            try:
                self.work()
            except:
                type, value, traceback = sys.exc_info()
                print "xgw: Unexpected exception in thread %s: %s" % (self.getName(), value)
