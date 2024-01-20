# API Reference
All data types that you interact with are exposed in `gestures.py`. The output of this API is a constant stream of `GestureMessages`:
```python
class GestureMessage:
    def __init__(self, x: int, y: int, gesture: str):
        self.x = x
        self.y = y
        self.gesture = gesture
```

Here, `x` and `y` are `int`s representing a relative position on the screen. These are scaled to the dimensions passed along during initialization. `gesture` is a string corresponding to a possible gesture. You can see the possible gestures in `possible_gesture_map`.

### Usage

First, create a callback that will process the data received by the library:
```python
def process_data(data: GestureMessage):
    print("X:" x, "Y:", y)
    print("Gesture:", data.gesture)
```

Now, create a `GestureWrapper`. Pass a tuple representing your desired dimensions (width, height). You can then obtain the stream representing MediaPipe's HandLandmarker:

```python
wrapper = GestureWrapper((100, 100))
stream = wrapper.create_stream(process_data)
```

Once you have that, it's just a matter of starting the stream! You should probably put this in its own thread. Whenever new data is available (often multiple times a second), a GestureMessage will be sent to `process_data`.

```python
asyncio.run(stream.begin_read())
```