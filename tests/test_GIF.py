from io import BytesIO
from pathlib import Path
from itertools import zip_longest

from PIL import Image

from gif import GIF


def compare(gif: GIF, num: int):
    test_file = BytesIO()
    gif.save(test_file)
    test_file.seek(0)
    test_gif = Image.open(test_file)

    result_gif = Image.open(
        Path(
            "tests",
            "result_images",
            "test_GIF",
            f"{num}",
            f"test_GIF_{num}.gif",
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


# noinspection PyPep8Naming
def test_GIF():
    gif = GIF(debug=False, progress_bar=False)
    gif.debug_template = Path(
        "tests",
        "debug_images",
        "test_GIF",
        "1",
        "test_GIF_1_{fragment_index}.png",
    )

    # add_text_fragment
    gif.add_text_fragment("text fragment", intro=True, outro=True)

    # add_image_fragment
    text_image = gif.process_text_image(
        gif.generate_text_image("text image"),
        intro=True,
        outro=True,
    )
    text_image.save("tests/tests_data/test_GIF/1/text_image.png")
    gif.add_image_fragment("tests/tests_data/test_GIF/1/text_image.png")

    gif.add_image_fragment(text_image)

    # add_gif_fragment
    with GIF(
        save_path="tests/tests_data/test_GIF/1/gif1.gif",
        progress_bar=False,
    ) as temp_gif:
        temp_gif.add_text_fragment("gif 1")

    gif.add_gif_fragment("tests/tests_data/test_GIF/1/gif1.gif")

    with BytesIO() as temp_file:
        with GIF(save_path=temp_file, progress_bar=False) as temp_gif:
            temp_gif.add_text_fragment("gif 2")

        temp_file.seek(0)
        gif.add_gif_fragment(temp_file)

    # gif.save("tests/result_images/test_GIF/1/test_GIF_1.gif")
    assert compare(gif, 1)
