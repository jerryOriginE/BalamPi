from ultralytics import YOLO
import cv2


class WasteAI:

    def __init__(
        self,
        model_path,
        camera_index=0,
        confidence_threshold=0.90,
        stable_frames=10
    ):

        self.model = YOLO(model_path)

        self.cap = cv2.VideoCapture(camera_index)

        self.confidence_threshold = confidence_threshold
        self.stable_frames = stable_frames

        self.last_label = None
        self.counter = 0

    def detect(self):
        """
        Returns:
            Plastic
            Metal
            Paper/Cardbord
            Tetrabrik

        or

            None
        """

        ret, frame = self.cap.read()

        if not ret:
            return None

        result = self.model(
            frame,
            verbose=False
        )[0]

        if result.probs is None:
            return None

        label = result.names[
            result.probs.top1
        ]

        confidence = float(
            result.probs.top1conf
        )

        if confidence < self.confidence_threshold:
            self._reset()
            return None

        if label.lower() == "nothing":
            self._reset()
            return None

        if label == self.last_label:
            self.counter += 1
        else:
            self.last_label = label
            self.counter = 1

        if self.counter < self.stable_frames:
            return None

        detected_label = label

        self._reset()

        print(
            f"Detected {detected_label} "
            f"({confidence:.2f})"
        )

        return detected_label

    def _reset(self):
        self.last_label = None
        self.counter = 0

    def release(self):
        if self.cap:
            self.cap.release()