import cv2
import mediapipe as mp

# Create a MediaPipe Hands object
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Video capture
vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(frame_rgb)

    # Draw the hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()






# import mediapipe as mp
# import cv2
# #from mediapipe.tasks import python
# #from mediapipe.tasks.python import vision

# # define a video capture object 
# vid = cv2.VideoCapture(0) 

# # MediaPipe inits
# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
# VisionRunningMode = mp.tasks.vision.RunningMode

# # Create a hand landmarker instance with the live stream mode:
# def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('hand landmarker result: {}'.format(result))

# # more mediapipe init stuff
# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path='model/hand_landmarker.task'),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)

# # where we use the landmarker
# with HandLandmarker.create_from_options(options) as landmarker:
#     # The landmarker is initialized. Use it here.
#     # ...
#     # Use OpenCV’s VideoCapture to start capturing from the webcam.

#     # Create a loop to read the latest frame from the camera using VideoCapture#read()

#     # Convert the frame received from OpenCV to a MediaPipe’s Image object.
#     # mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)

#     while(True):
#         # # TODO: Make sure to add some way to break out of this loop
#         # # Capture the video frame 
#         # # by frame 
#         # ret, frame = vid.read()

#         # #mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)
#         # # This converted image is not used here, just for conceptual understanding purposes
#         # mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

#         # print_result(HandLandmarkerResult, mp_image, 0)
#         # Capture the video frame
#         ret, frame = vid.read()
#         if not ret:
#             break

#         # Convert the frame from OpenCV to a MediaPipe Image
#         # Note: You may need to convert the frame's color space from BGR to RGB
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

#         # Process the image with the hand landmarker
#         result = landmarker.process(mp_image)

#         # Call the print_result function with the actual result
#         print_result(result, mp_image, 0)
        
#         # Display the resulting frame 
#         # cv2.imshow('frame', frame) 
        
#         # the 'q' button is set as the 
#         # quitting button you may use any 
#         # desired button of your choice 
#         # if cv2.waitKey(1) & 0xFF == ord('q'): 
#         #     break
    
#     # After the loop release the cap object 
#     vid.release() 
#     # Destroy all the windows 
#     cv2.destroyAllWindows() 

