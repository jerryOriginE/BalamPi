import time

class SessionManager:
    def __init__(self):
        self.user = None
        self.active = False
        self.last_active = 0

    def start(self, user):
        self.user = user
        self.active = True

        self.touch()

    def touch(self):
        self.last_active = time.time()

    def expired(self):
        return (time.time() - self.last_active) > 30
    
    def stop(self):
        self.user = None
        self.active = False
        