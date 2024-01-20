from enum import Enum
from functools import partial

from media_processing import FrameData, Landmarks
from utils import dist_2d

"""
To add a new gesture:
  1. add a function below, where given some FrameData, it checks if the gesture is being performed
  2. add the function to the enum GestureType below, above OPEN_HAND
  3. add the string representation to possible_gesture_map in gestures.py
"""


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


def check_for_index_extended(data) -> bool:
    # If the index finger's PIP is further from the wrist than the other finger's DIP
    wrist = data.fetch(Landmarks.WRIST)
    wx = wrist.x
    wy = wrist.y

    index = data.fetch(Landmarks.INDEX_FINGER_PIP)
    ix = index.x
    iy = index.y

    thumb = data.fetch(Landmarks.THUMB_IP)
    middle = data.fetch(Landmarks.MIDDLE_FINGER_DIP)
    ring = data.fetch(Landmarks.RING_FINGER_DIP)
    pinky = data.fetch(Landmarks.PINKY_FINGER_DIP)

    if dist_2d(ix, iy, wx, wy) < dist_2d(thumb.x, thumb.y, wx, wy):
        return False
    if dist_2d(ix, iy, wx, wy) < dist_2d(middle.x, middle.y, wx, wy):
        return False
    if dist_2d(ix, iy, wx, wy) < dist_2d(ring.x, ring.y, wx, wy):
        return False
    if dist_2d(ix, iy, wx, wy) < dist_2d(pinky.x, pinky.y, wx, wy):
        return False

    return True


def check_for_open_hand(data) -> bool:
    return True


# OPEN_HAND is the default gesture for your hand to be in
# If nothing else matches, it will default to that
class GestureType(Enum):
    CLOSED_FIST = partial(check_for_closed_fist)
    INDEX_EXTENDED = partial(check_for_index_extended)
    OPEN_HAND = partial(check_for_open_hand)
    NO_HAND = -1


class GestureDetector:
    def get_gesture(self, frame_data: FrameData) -> GestureType:
        if frame_data.empty:
            return GestureType.NO_HAND
        for gesture in GestureType:
            if gesture.value(frame_data):
                return gesture
