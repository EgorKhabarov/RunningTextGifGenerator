"""
Download zip from https://github.com/Felixoofed/badapple-frames/blob/main/frames.zip
"""

import io
import math
import zipfile

from PIL import Image

from gif import GIF


c = 1.3333333333333333
x = 90
y = math.ceil(x / c)
gif = GIF(columns=x, rows=y)
gif.color_config["color_pixel_off_light"] = "#EFEFEF"
gif.color_config["color_pixel_off_dark"] = "#BFBFBF"
gif.color_config["color_pixel_on_light"] = "#2F2F2F"
gif.color_config["color_pixel_on_dark"] = "#000000"


with zipfile.ZipFile("frames.zip", "r") as zip_ref:
    for i in range(1, 6573, 3):
        filename = f"frames/output_{i:0>4}.jpg"
        with zip_ref.open(filename) as file:
            image = Image.open(io.BytesIO(file.read()))
            gif.add_image_fragment(
                image_path=image.resize((x, y)),
                duration=50,
            )

gif.save(path="bad_apple.gif")
