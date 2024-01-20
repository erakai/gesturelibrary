from gestures import GestureWrapper


wrapper = GestureWrapper((100, 100))
stream = wrapper.get_stream()

while True:
    print("\n\nPress Enter: ", end="")
    text = input()
    print("GESTURE MESSAGE: ", stream.read())
