import mediapipe as mp
import cv2
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

vid = cv2.VideoCapture(0)


# Create a hand landmarker instance with the live stream mode:
def print_result(
    result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int
):
    print("hand landmarker result: {}".format(result))


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="../model/hand_landmarker.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
)
with HandLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
    # ...
    while True:
        ret, frame = vid.read()
        if not ret:
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        timestamp = int(time.perf_counter_ns())

        landmarker.detect_async(mp_image, timestamp)

    vid.release()
    cv2.destroyAllWindows()
