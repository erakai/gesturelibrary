from coord_translator import CoordTranslator
from gesture_detector import GestureDetector, GestureType
from media_processing import MediaProcessor


class GestureMessage:
    def __init__(self, x: int, y: int, gesture: GestureType):
        self.x = x
        self.y = y
        self.gesture = gesture


class GestureStream:
    def __init__(self, translator, detector):
        self.translator = translator
        self.detector = detector
        self.processor = MediaProcessor()

    def read(self) -> GestureMessage:
        frame_data = self.processor.process_frame()
        print("FOUND DATA: ", frame_data)

        print("COORD TRANSLATOR: ", self.translator.translate_coords(frame_data))
        print("GESTURE DETECTOR: ", self.detector.get_gesture(frame_data))

    def close(self) -> None:
        self.stream.close()
        self.processor.close()


class GestureWrapper:
    def __init__(self, webcam_dimensions: tuple[int, int]):
        self.dimensions = (0, 0)
        self.stream = None
        self.translator = CoordTranslator(webcam_dimensions)
        self.detector = GestureDetector()

    def get_stream(self) -> GestureStream:
        if self.stream is not None:
            self.stream.close()

        self.stream = GestureStream(self.translator, self.detector)

        return self.stream

    def close(self) -> None:
        self.stream.close()
