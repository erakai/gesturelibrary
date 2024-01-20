from asyncio import sleep
import mediapipe as mp
import cv2


class MediaProcessor:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands()

    def process_frame(self):
        ret, frame = self.video.read()

        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        return results.multi_hand_landmarks

    def close(self):
        self.video.release()
