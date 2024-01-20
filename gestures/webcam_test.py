# TODO: 
# all go inside a class
# while run == 1
# run this loop and contiually fetches new info

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
    
    print(results.multi_hand_landmarks)

    # Show the frame
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()