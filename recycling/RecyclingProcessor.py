# recycling/RecyclingProcessor.py
import threading

class RecyclingProcessor:
    def __init__(
            self, 
            ars,
            api,
            session,
            lcd,
            cooldown
    ):
        self.ars = ars
        self.api = api
        self.session = session
        self.lcd = lcd
        self.cooldown = cooldown

        self.lock = threading.Lock()

    def process(self, waste_type):
        if not self.lock.acquire(blocking=False):
            return False
        
        try:
            if not self.session.active:
                return
            
            if not self.cooldown.allowed():
                return
            
            self.session.touch()

            self.ars.process(waste_type)

            result = self.api.award_points(
                self.session.user["id"],
                waste_type
            )

            points = result.get(
                "pointsAwarded",
                "?"
            )

            self.lcd.show(
                f"{waste_type} +{points}"
            )
            
        finally:
            self.lock.release()
