# core/StateMachine.py
from enum import Enum

class State(Enum):
    IDLE = "IDLE"
    WAITING_QR = "WAITING_QR"
    AUTHENTICATING = "AUTHENTICATING"
    ACTIVE = "ACTIVE"
    PROCESSING = "PROCESSING"