# recycling/CooldownManager.py
import time

class CooldownManager:
    def __init__(self, cooldown=5):
        self.cooldown = cooldown
        self.last_detection = 0

    def allowed(self):
        now = time.time()

        if now - self.last_detection < self.cooldown:
            return False
        
        self.last_detection = now
        return True