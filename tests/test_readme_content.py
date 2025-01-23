from gif import GIF
from tests.utils import compare_gif


def test_readme_content():
    gif = GIF(columns=20, rows=20, progress_bar=False)
    gif.add_image_fragment(
        image_path="readme_content/frog_jump.png",
        direction="left",
        duration=100,
        speed=21,
    )
    gif.color_config["color_pixel_off_light"] = "#438600"
    gif.color_config["color_pixel_off_dark"] = "#346800"
    gif.color_config["color_pixel_on_light"] = "#B9FF73"
    gif.color_config["color_pixel_on_dark"] = "#6AD500"
    assert compare_gif(gif, "readme_content/frog_jump.gif")

    gif = GIF(columns=22, rows=24, progress_bar=False)
    gif.add_image_fragment(
        image_path="readme_content/dino.png",
        direction="up",
        duration=100,
        speed=24,
    )
    assert compare_gif(gif, "readme_content/dino.gif")
