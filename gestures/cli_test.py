import asyncio
from gestures import GestureWrapper
from gestures import GestureMessage


def process_data(data: GestureMessage):
    print("Message:", data)


# (x, y), fps
wrapper = GestureWrapper((100, 100))
stream = wrapper.create_stream(process_data)

asyncio.run(stream.begin_read())
