from coord_translator import CoordTranslator
from gesture_detector import GestureDetector, GestureType
from media_processing import FrameData, MediaProcessor


class GestureMessage:
    def __init__(self, x: int, y: int, gesture: GestureType):
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
        print("Coords:", self.translator.translate_coords(data))
        print("Gesture:", self.detector.get_gesture(data))
        msg = GestureMessage(0, 0, GestureType.UNRECOGNIZED)
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
