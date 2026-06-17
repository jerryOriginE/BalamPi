import random
import shutil
from pathlib import Path

SOURCE = Path("dataset-resized")
TARGET = Path("waste_dataset")

CLASSES = ["paper", "plastic", "metal"]

for cls in CLASSES:
    files = list((SOURCE / cls).glob("*"))

    random.shuffle(files)

    split_idx = int(len(files) * 0.8)

    train_files = files[:split_idx]
    val_files = files[split_idx:]

    for subset, subset_files in [
        ("train", train_files),
        ("val", val_files),
    ]:
        out_dir = TARGET / subset / cls
        out_dir.mkdir(parents=True, exist_ok=True)

        for f in subset_files:
            shutil.copy(f, out_dir / f.name)

print("Done.")
