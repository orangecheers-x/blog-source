from PIL import Image
file = "test.jpeg"
img = Image.open(file)
img = img.convert("RGB")
for i in [20, 30, 40, 50, 60, 70]:
    img.save((file + str(i) + ".webp"), "webp", quality=i)
