import io
from enum import Enum
from gestures.coord_translating import CoordTranslator

from gestures.gesture_detector import GestureDetector, GestureType


class GestureMessage:
    def __init__(self, x: int, y: int, gesture: GestureType):
        self.x = x
        self.y = y
        self.gesture = gesture


class GestureStream:
    def __init__(self, translator, detector):
        self.translator = translator
        self.detector = detector

    def read(self) -> GestureMessage:
        pass

    def close(self) -> None:
        self.stream.close()


class GestureWrapper:
    def __init__(self, webcam_dimensions: tuple[int, int]):
        self.dimensions = (0, 0)
        self.stream = None
        self.translator = CoordTranslator(webcam_dimensions)
        self.detector = GestureDetector()

    def get_stream(self) -> GestureStream:
        if self.stream is not None:
            self.close()
        self.stream = GestureStream(self.translator, self.detector)

        return self.stream

    def close(self) -> None:
        self.stream.close()
        # self.processor.quit()
