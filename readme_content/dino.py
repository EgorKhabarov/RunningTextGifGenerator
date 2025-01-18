from gif import GIF


gif = GIF(columns=22, rows=24)
gif.add_image_fragment(
    image_path="dino.png",
    direction="up",
    duration=100,
    speed=24,
)
gif.save(path="dino.gif")
