import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    data, points, _ = detector.detectAndDecode(frame)

    if data:
        print(f"QR Code detected: {data}")
        cv2.putText(
            frame,
            f"QR Code: {data}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("QR Code Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()