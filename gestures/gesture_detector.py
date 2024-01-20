from enum import Enum

from media_processing import FrameData


def check_for_open_hand(frame_data) -> bool:
    pass


def check_for_closed_fist(frame_data) -> bool:
    pass


class GestureType(Enum):
    OPEN_HAND = staticmethod(check_for_open_hand)
    CLOSED_FIRST = staticmethod(check_for_closed_fist)
    UNRECOGNIZED = staticmethod(lambda x: True)


class GestureDetector:
    def get_gesture(self, frame_data: FrameData) -> GestureType:
        for gesture in GestureType:
            if gesture(frame_data):
                return gesture
        return GestureType.UNRECOGNIZED
