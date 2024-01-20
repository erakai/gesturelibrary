from coord_translator import CoordTranslator
from gesture_detector import GestureDetector, GestureType
from media_processing import FrameData, MediaProcessor


possible_gesture_map = {
    GestureType.OPEN_HAND: "OPEN_HAND",
    GestureType.CLOSED_FIST: "CLOSED_FIST",
    GestureType.NO_HAND: "NO_HAND",
}


class GestureMessage:
    def __init__(self, x: int, y: int, gesture: str):
        self.x = x
        self.y = y
        self.gesture = gesture


class GestureStream:
    def __init__(self, translator, detector, process_data):
        self.translator = translator
        self.detector = detector
        self.process_data = process_data
        self.processor = MediaProcessor(self.process_into_messages)

    async def begin_read(self):
        await self.processor.begin_processing()

    def process_into_messages(self, data: FrameData):
        msg = GestureMessage(
            0, 0, possible_gesture_map[self.detector.get_gesture(data)]
        )
        self.process_data(msg)

    def close(self) -> None:
        self.processor.close()


class GestureWrapper:
    def __init__(self, webcam_dimensions: tuple[int, int]):
        self.dimensions = (0, 0)
        self.stream = None
        self.translator = CoordTranslator(webcam_dimensions)
        self.detector = GestureDetector()

    def create_stream(self, process_data: callable) -> GestureStream:
        if self.stream is not None:
            self.stream.close()

        self.stream = GestureStream(
            self.translator,
            self.detector,
            process_data,
        )

        return self.stream

    def close(self) -> None:
        self.stream.close()
