from gif import GIF


with GIF(20, 20, save_path="frog_jump.gif") as gif:
    gif.color_config["color_pixel_off_light"] = "#438600"
    gif.color_config["color_pixel_off_dark"] = "#346800"
    gif.color_config["color_pixel_on_light"] = "#B9FF73"
    gif.color_config["color_pixel_on_dark"] = "#6AD500"
    gif.add_image_fragment("frog_jump.png", duration=100, speed=21)
