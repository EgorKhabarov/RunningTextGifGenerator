from gif import GIF
from tests.utils import compare_gif


def test_readme_content():
    gif = GIF(columns=22, rows=24, progress_bar=False)
    gif.add_image_fragment(
        image_path="readme_content/dino.png",
        direction="up",
        duration=100,
        speed=24,
    )
    assert compare_gif(gif, "readme_content/dino.gif")

    gif = GIF(columns=20, rows=20, progress_bar=False)
    gif.add_image_fragment(
        image_path="readme_content/frog_jump.png",
        direction="left",
        duration=100,
        speed=21,
    )
    assert compare_gif(gif, "readme_content/frog_jump.gif")
