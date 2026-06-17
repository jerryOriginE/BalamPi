from ultralytics import YOLO

model = YOLO("yolo11n-cls.pt")

model.train(
    data="waste_dataset",
    epochs=30,
    imgsz=224,
    batch=32
)
