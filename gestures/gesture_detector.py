from enum import Enum


class GestureType(Enum):
    OPEN_HAND = 1
    CLOSED_FIRST = 2


class GestureDetector:
    def __init__(self):
        pass

    def get_gesture(self, frame_data):
        pass
