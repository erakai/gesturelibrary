from time import time, perf_counter_ns
import asyncio
from enum import Enum
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands


class MediaProcessor:
    def __init__(self, data_callback: callable):
        self.video = cv2.VideoCapture(0)
        self.video_start = perf_counter_ns()
        self.data_callback = data_callback

    def begin_processing(self):
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1,
        ) as hands:
            while True:
                ret, frame = self.video.read()

                if not ret:
                    print("Error getting frame...")
                    continue

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame)

                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    self.convert_data(hand_landmarks)

    def convert_data(self, results):
        converted = FrameData(results)
        self.data_callback(converted)

    def close(self):
        self.video.release()


class Landmarks(Enum):
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_FINGER_MCP = 17
    PINKY_FINGER_PIP = 18
    PINKY_FINGER_DIP = 19
    PINKY_FINGER_TIP = 20


class Coords:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class FrameData:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.empty = False
        self.data = {}

        self._create_data()

    def _create_data(self):
        if self.empty:
            return
        vals = getattr(self.raw_data, "landmark")
        for landmark in Landmarks:
            val = vals[landmark.value]
            x = getattr(val, "x")
            y = getattr(val, "y")
            z = getattr(val, "z")
            self.data[landmark] = Coords(x, y, z)

    def fetch(self, landmark: Landmarks) -> Coords:
        if self.empty:
            return Coords(-1, -1, -1)
        return self.data[landmark]
