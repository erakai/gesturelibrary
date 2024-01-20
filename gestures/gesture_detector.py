from enum import Enum
from functools import partial

from media_processing import FrameData, Landmarks
from utils import dist_2d


def check_for_closed_fist(data) -> bool:
    # If your index/middle/ring/pinky fingers's TIPs are closer to your wrist than their PIP
    # we must have a closed fist

    wrist = data.fetch(Landmarks.WRIST)
    wx = wrist.x
    wy = wrist.y

    indext = data.fetch(Landmarks.INDEX_FINGER_TIP)
    indexp = data.fetch(Landmarks.INDEX_FINGER_PIP)

    middlet = data.fetch(Landmarks.MIDDLE_FINGER_TIP)
    middlep = data.fetch(Landmarks.MIDDLE_FINGER_PIP)

    ringt = data.fetch(Landmarks.RING_FINGER_TIP)
    ringp = data.fetch(Landmarks.RING_FINGER_PIP)

    pinkyt = data.fetch(Landmarks.PINKY_FINGER_TIP)
    pinkyp = data.fetch(Landmarks.PINKY_FINGER_PIP)

    if dist_2d(indext.x, indext.y, wx, wy) > dist_2d(indexp.x, indexp.y, wx, wy):
        return False
    if dist_2d(middlet.x, middlet.y, wx, wy) > dist_2d(middlep.x, middlep.y, wx, wy):
        return False
    if dist_2d(ringt.x, ringt.y, wx, wy) > dist_2d(ringp.x, ringp.y, wx, wy):
        return False
    if dist_2d(pinkyt.x, pinkyt.y, wx, wy) > dist_2d(pinkyp.x, pinkyp.y, wx, wy):
        return False

    return True


def check_for_open_hand(data) -> bool:
    return True


# OPEN_HAND is the default gesture for your hand to be in
# If nothing else matches, it will default to that
class GestureType(Enum):
    CLOSED_FIST = partial(check_for_closed_fist)
    OPEN_HAND = partial(check_for_open_hand)
    NO_HAND = -1


class GestureDetector:
    def get_gesture(self, frame_data: FrameData) -> GestureType:
        if frame_data.empty:
            return GestureType.NO_HAND
        for gesture in GestureType:
            if gesture.value(frame_data):
                return gesture
