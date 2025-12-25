import json
import os

IMAGE_DIR = "images"
OUTPUT = "images.json"
EXTENSIONS = (".png", ".jpg", ".jpeg")

files = sorted(
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(EXTENSIONS)
)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(files, f, indent=2)

print(f"Generated {OUTPUT} with {len(files)} images.")
