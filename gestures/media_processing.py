from time import time, perf_counter_ns
import asyncio
from enum import Enum
import mediapipe as mp
import cv2

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class MediaProcessor:
    def __init__(self, data_callback: callable):
        self.video = cv2.VideoCapture(0)
        self.video_start = perf_counter_ns()
        self.data_callback = data_callback

    async def begin_processing(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path="../model/hand_landmarker.task"),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.convert_data,
        )
        with HandLandmarker.create_from_options(options) as landmarker:
            while True:
                ret, frame = self.video.read()

                if not ret:
                    print("Error getting frame...")
                    continue

                # Calculate frame time since last frime for mediapipe
                new_time = perf_counter_ns()
                frame_time = int((new_time - self.video_start) / 1000000)
                print("\nFrame Time:", frame_time)

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                landmarker.detect_async(mp_image, frame_time)

    def convert_data(self, results: HandLandmarkerResult, image, time):
        print("RAW DATA: ", results)
        converted = FrameData(results.hand_landmarks)
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
    INDEX_FIGHER_PIP = 6
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
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20


class Coords:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class FrameData:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.empty = len(self.raw_data) == 0
        self.data = {}

        self.create_data()

    def create_data(self):
        if self.empty:
            return
        for landmark in Landmarks:
            vals = self.raw_data[0][landmark.value]
            self.data[landmark] = Coords(vals.x, vals.y, vals.z)

    def fetch_data(self, landmark: Landmarks) -> Coords:
        if self.empty:
            return (-1, -1, -1)
        return self.data[landmark]
