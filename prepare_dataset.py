import os
import random
import shutil
from pathlib import Path

# Source dataset
SOURCE_DIR = Path("trashnet/dataset-resized")
#SOURCE_DIR = Path("barbiedata")

# Output dataset for YOLO Classification
OUTPUT_DIR = Path("waste_dataset")

TRAIN_RATIO = 0.8

random.seed(42)

train_dir = OUTPUT_DIR / "train"
val_dir = OUTPUT_DIR / "val"

train_dir.mkdir(parents=True, exist_ok=True)
val_dir.mkdir(parents=True, exist_ok=True)

image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

for class_folder in SOURCE_DIR.iterdir():
    if not class_folder.is_dir():
        continue

    class_name = class_folder.name

    print(f"\nProcessing {class_name}...")

    train_class_dir = train_dir / class_name
    val_class_dir = val_dir / class_name

    train_class_dir.mkdir(parents=True, exist_ok=True)
    val_class_dir.mkdir(parents=True, exist_ok=True)

    images = [
        f for f in class_folder.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    random.shuffle(images)

    split_idx = int(len(images) * TRAIN_RATIO)

    train_images = images[:split_idx]
    val_images = images[split_idx:]

    for img in train_images:
        shutil.copy2(img, train_class_dir / img.name)

    for img in val_images:
        shutil.copy2(img, val_class_dir / img.name)

    print(f"  Train: {len(train_images)}")
    print(f"  Val:   {len(val_images)}")

print("\nDataset preparation complete!")