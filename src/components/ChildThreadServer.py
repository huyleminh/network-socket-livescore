import threading

Thread = threading.Thread

class ChildThreadServer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        pass