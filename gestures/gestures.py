from gestures.coord_translator import CoordTranslator
from gestures.gesture_detector import GestureDetector, GestureType
from gestures.media_processing import Coords, FrameData, Landmarks, MediaProcessor


possible_gesture_map = {
    GestureType.OPEN_HAND: "OPEN_HAND",
    GestureType.CLOSED_FIST: "CLOSED_FIST",
    GestureType.INDEX_EXTENDED: "INDEX_EXTENDED",
    GestureType.NO_HAND: "NO_HAND",
    GestureType.RING_EXTENDED: "RING_EXTENDED",
    GestureType.MIDDLE_EXTENDED: "MIDDLE_EXTENDED",
    GestureType.PINKY_EXTENDED: "PINKY_EXTENDED",
    # GestureType.BEAST_BOY: "BEAST_BOY"
}


class GestureMessage:
    def __init__(self, x: int, y: int, px: int, py: int, gesture: str):
        self.x = x
        self.y = y
        self.pointer_x = px
        self.pointer_y = py
        self.gesture = gesture


class GestureStream:
    def __init__(self, translator, detector, process_data, dimensions):
        self.translator = translator
        self.detector = detector
        self.process_data = process_data
        self.processor = MediaProcessor(self.process_into_messages)
        self.dimensions = dimensions

    def begin_read(self):
        self.processor.begin_processing()

    def process_into_messages(self, data: FrameData):
        x, y = self.translator.translate_coords(data)
        pointer = Coords(0, 0, 0)
        if not data.empty:
            pointer = data.fetch(Landmarks.INDEX_FINGER_TIP)
        msg = GestureMessage(
            x,
            y,
            self.dimensions[0] - (pointer.x * self.dimensions[0]),
            pointer.y * self.dimensions[1],
            possible_gesture_map[self.detector.get_gesture(data)],
        )
        self.process_data(msg)

    def close(self) -> None:
        self.processor.close()


class GestureWrapper:
    def __init__(self, webcam_dimensions: tuple[int, int]):
        self.dimensions = webcam_dimensions
        self.stream = None
        self.translator = CoordTranslator(webcam_dimensions)
        self.detector = GestureDetector()

    def create_stream(self, process_data: callable) -> GestureStream:
        if self.stream is not None:
            self.stream.close()

        self.stream = GestureStream(
            self.translator, self.detector, process_data, self.dimensions
        )

        return self.stream

    def close(self) -> None:
        self.stream.close()
