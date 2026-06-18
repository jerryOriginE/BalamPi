from ultralytics import YOLO
import cv2
from time import sleep
from controllers.RecycleController import ARS, Position
from collections import Counter
import numpy as np

def show_processing(label):
    screen = np.zeros((720, 1280, 3), dtype=np.uint8)

    cv2.putText(
        screen,
        "PROCESSING ITEM",
        (250, 250),
        cv2.FONT_HERSHEY_DUPLEX,
        2,
        (0, 255, 255),
        3
    )

    cv2.putText(
        screen,
        label.upper(),
        (350, 400),
        cv2.FONT_HERSHEY_DUPLEX,
        3,
        (0, 255, 0),
        5
    )

    cv2.imshow("ARS Status", screen)
    cv2.waitKey(1)

trash_counts = Counter()

ARS_system = ARS()
ARS_system.change_trash_data("plastic", Position.BACK_RIGHT)
ARS_system.change_trash_data("trash", Position.FRONT_LEFT)
ARS_system.change_trash_data("cardboard", Position.BACK_LEFT)
ARS_system.change_trash_data("metal", Position.FRONT_RIGHT)

ARS_system.calibrate_system()

model = YOLO("ars.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False) # shut the logs

    result = results[0]

    class_id = result.probs.top1
    confidence = float(result.probs.top1conf)

    label = result.names[class_id]

    # showcase whatever it is seing

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

    # showcase if its above 85% confidence showing what it think if its, if is not sure put that then
    if confidence > 0.65 and label != "nothing":
        trash_counts[label] += 1

        cv2.putText(
            frame,
            f"Prediction: {label}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.waitKey(1)
        cap.release()

        show_processing(label)
        ARS_system.process_trash(label)  # send the detected trash type to the ARS system for processing
        
        cv2.destroyWindow("ARS Status")
        cap = cv2.VideoCapture(0)

    elif confidence >= 0.60 and label != "nothing":
        cv2.putText(
            frame,
            f"Basura",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        #trash(cap, "trash")
    else:
        cv2.putText(
            frame,
            "Prediction: Not sure",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

    # watermark ©BALAM - ARS 2026
    cv2.putText(
        frame,
        "©BALAM - ARS 2026",
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    cv2.imshow("Waste Classifier", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\n=== Sorting Summary ===")

total = sum(trash_counts.values())

for item, count in trash_counts.items():
    print(f"{item}: {count}")

print(f"\nTotal items sorted: {total}")