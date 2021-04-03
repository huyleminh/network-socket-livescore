import threading

Thread = threading.Thread

class UserThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        pass