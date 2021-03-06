import threading
import sys
import six


class ThreadHandler(object):
    def __init__(self, name, callable, *args, **kwargs):
        # Set up exception handling
        self.exception = None
        self.exc_info = None

        def wrapper(*args, **kwargs):
            try:
                callable(*args, **kwargs)
            except BaseException as e:
                self.exception = e
                self.exc_info = sys.exc_info()
        # Kick off thread
        thread = threading.Thread(None, wrapper, name, args, kwargs)
        thread.setDaemon(True)
        thread.start()
        # Make thread available to instantiator
        self.thread = thread

    def raise_if_needed(self):
        if self.exception:
            six.reraise(*self.exc_info)
