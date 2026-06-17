from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("best.pt")

# Open Raspberry Pi camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run AI prediction
    results = model(frame)

    # Get prediction
    result = results[0]

    class_id = result.probs.top1
    confidence = float(result.probs.top1conf)

    label = result.names[class_id]

    # Display result
    text = f"{label}: {confidence*100:.1f}%"

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Waste Classifier", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
