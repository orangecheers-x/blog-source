from PIL import Image
import PIL
import os
import pathlib
import re

dirlist = os.walk("./source/img")
for root, dirs, files in dirlist:
    root = pathlib.Path(root)
    for file in files:
        if (file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")) and not os.path.exists(root / (file + ".webp")):
            print(root / file)
            img = Image.open(root / file)
            img = img.convert("RGB")
            img.save(root / (file + ".webp"), "webp", quality=70)

dirlist = os.listdir("./source/_posts")
for file in dirlist:
    if file.endswith(".md"):
        with open("./source/_posts/" + file, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"!\[(.*)\]\((.*\.(jpg|png|jpeg))\)",
                         r"![\1](\2.webp)", content)
        with open("./source/_posts/" + file, "w", encoding="utf-8") as f:
            f.write(content)
