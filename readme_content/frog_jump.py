from gif import GIF


with GIF(20, 20, save_path="frog_jump.gif") as gif:
    gif.add_image_fragment("frog_jump.png", duration=100, speed=21)
