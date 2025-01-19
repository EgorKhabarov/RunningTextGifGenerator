from io import BytesIO
from pathlib import Path
from itertools import zip_longest

from PIL import Image

from gif import GIF


def compare(gif: GIF, num: int, intro: bool, outro: bool):
    test_file = BytesIO()
    gif.save(test_file)
    test_file.seek(0)
    test_gif = Image.open(test_file)

    result_gif = Image.open(
        Path(
            "tests",
            "result_images",
            "test_direction",
            f"{num}",
            f"test_direction_{num}_{intro}_{outro}.gif",
        )
    )

    test_frames = GIF.extract_gif_frames(test_gif)
    result_frames = GIF.extract_gif_frames(result_gif)
    for (test_image, _), (result_image, _) in zip_longest(test_frames, result_frames):
        if None in (test_image, result_image):
            return False

        if test_image != result_image:
            return False
    return True


def test_direction():
    gif = GIF(debug=False, progress_bar=False)

    intro = True
    outro = True
    gif.debug_template = Path(
        "tests",
        "debug_images",
        "test_direction",
        "1",
        f"test_direction_1_{intro}_{outro}_{{fragment_index}}.png",
    )
    gif.add_text_fragment(
        f"--{intro=};{outro=}--",
        intro=False,
        outro=False,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "left",
        intro=intro,
        outro=outro,
        direction="left",
        duration=66,
    )
    gif.add_text_fragment(
        "up",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right",
        intro=intro,
        outro=outro,
        direction="right",
        duration=66,
    )
    gif.add_text_fragment(
        "down",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    gif.add_text_fragment(
        "left biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "up biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="right",
        duration=50,
    )
    gif.add_text_fragment(
        "down biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    # gif.save(f"tests/result_images/test_direction/1/test_direction_1_{intro}_{outro}.gif")
    assert compare(gif, 1, intro, outro)

    intro = True
    outro = False
    gif.debug_template = Path(
        "tests",
        "debug_images",
        "test_direction",
        "2",
        f"test_direction_2_{intro}_{outro}_{{fragment_index}}.png",
    )
    gif.add_text_fragment(
        f"--{intro=};{outro=}--",
        intro=False,
        outro=False,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "left",
        intro=intro,
        outro=outro,
        direction="left",
        duration=66,
    )
    gif.add_text_fragment(
        "up",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right",
        intro=intro,
        outro=outro,
        direction="right",
        duration=66,
    )
    gif.add_text_fragment(
        "down",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    gif.add_text_fragment(
        "left biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "up biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="right",
        duration=50,
    )
    gif.add_text_fragment(
        "down biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    # gif.save(f"tests/result_images/test_direction/2/test_direction_2_{intro}_{outro}.gif")
    assert compare(gif, 2, intro, outro)

    intro = False
    outro = True
    gif.debug_template = Path(
        "tests",
        "debug_images",
        "test_direction",
        "3",
        f"test_direction_3_{intro}_{outro}_{{fragment_index}}.png",
    )
    gif.add_text_fragment(
        f"--{intro=};{outro=}--",
        intro=False,
        outro=False,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "left",
        intro=intro,
        outro=outro,
        direction="left",
        duration=66,
    )
    gif.add_text_fragment(
        "up",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right",
        intro=intro,
        outro=outro,
        direction="right",
        duration=66,
    )
    gif.add_text_fragment(
        "down",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    gif.add_text_fragment(
        "left biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "up biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="up",
        duration=200,
    )
    gif.add_text_fragment(
        "right biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="right",
        duration=50,
    )
    gif.add_text_fragment(
        "down biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="down",
        duration=200,
    )
    # gif.save(f"tests/result_images/test_direction/3/test_direction_3_{intro}_{outro}.gif")
    assert compare(gif, 3, intro, outro)

    intro = False
    outro = False
    gif.debug_template = Path(
        "tests",
        "debug_images",
        "test_direction",
        "4",
        f"test_direction_4_{intro}_{outro}_{{fragment_index}}.png",
    )
    gif.add_text_fragment(
        f"--{intro=};{outro=}--",
        intro=False,
        outro=False,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "left",
        intro=intro,
        outro=outro,
        direction="left",
        duration=1000,
    )
    gif.add_text_fragment(
        "up",
        intro=intro,
        outro=outro,
        direction="up",
        duration=1000,
    )
    gif.add_text_fragment(
        "right",
        intro=intro,
        outro=outro,
        direction="right",
        duration=66,
    )
    gif.add_text_fragment(
        "down",
        intro=intro,
        outro=outro,
        direction="down",
        duration=1000,
    )
    gif.add_text_fragment(
        "left biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="left",
        duration=50,
    )
    gif.add_text_fragment(
        "up biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="up",
        duration=1000,
    )
    gif.add_text_fragment(
        "right biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="right",
        duration=50,
    )
    gif.add_text_fragment(
        "down biiiiiig teeexxxt",
        intro=intro,
        outro=outro,
        direction="down",
        duration=1000,
    )
    # gif.save(f"tests/result_images/test_direction/4/test_direction_4_{intro}_{outro}.gif")
    assert compare(gif, 4, intro, outro)
