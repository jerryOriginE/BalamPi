import cv2

# Open default camera (0)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame")
        break

    cv2.imshow("Camera Test", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
