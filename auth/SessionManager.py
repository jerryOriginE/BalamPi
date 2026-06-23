# auth/SessionManager.py
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
    
    def stop(self):
        self.user = None
        self.active = False
        self.last_active = 0

    def expired(self, timeout=30):
        if not self.actove:
            return False
        
        return (time.time() - self.last_active) > timeout