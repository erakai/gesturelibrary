# just for conceptual purposes, the method seen in this file can just be done in the media pipe file
# because the conversion is just one line so why add the overhead

# import the opencv library 
import cv2 
import mediapipe as mp
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    #mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)
    # This converted image is not used here, just for conceptual understanding purposes
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
  
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 


# # Somehow return the webcam data (idk what form that takes)
# def camera_stream():
#     pass