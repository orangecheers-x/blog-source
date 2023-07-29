from PIL import Image
import PIL
import os
import pathlib

dirlist = os.walk("./source/img")
for root, dirs, files in dirlist:
    root = pathlib.Path(root)
    for file in files:
        if file.endswith(".png") and not os.path.exists(root / file.replace(".png", ".webp")):
            print(root / file)
            img = Image.open(root / file)
            img = img.convert("RGB")
            img.save(root / file.replace(".png", ".webp"), "webp", quality=70)
