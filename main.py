import cv2

# Initialize the camera (0 is the default webcam)
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()
    
    # Check if frame was read successfully
    if not ret:
        break
        
    # Display the frame
    cv2.imshow('Webcam Feed', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()   
