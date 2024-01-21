import asyncio
from gestures.gestures import GestureWrapper, GestureMessage


def process_data(data: GestureMessage):
    print("Gesture:", data.gesture)
    print("Coords: ", data.x, data.y)


# (x, y), fps
wrapper = GestureWrapper((100, 100))
stream = wrapper.create_stream(process_data)

asyncio.run(stream.begin_read())

# bugs: Thumb