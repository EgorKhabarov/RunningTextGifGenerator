from io import BytesIO

# noinspection PyPackageRequirements
import pytest

from gif import GIF
from tests.utils import compare_gif


# noinspection PyPep8Naming
@pytest.mark.parametrize(
    "num, loop, repeat",
    (
        (1, 0, 1),
        (2, 2, 2),
    ),
)
def test_GIF(num: int, loop: int, repeat: int):
    gif = GIF(debug=False, progress_bar=False, loop=loop)
    gif.debug_path = (
        f"tests/debug_images/test_GIF/{num}/test_GIF_{num}_{{fragment_index}}.png"
    )

    # add_text_fragment
    gif.add_text_fragment("text fragment", intro=True, outro=True, repeat=repeat)

    # add_image_fragment
    text_image = gif.process_text_image(
        gif.generate_text_image("text image"),
        intro=True,
        outro=True,
    )
    text_image.save(f"tests/tests_data/test_GIF/{num}/text_image.png")
    gif.add_image_fragment(
        f"tests/tests_data/test_GIF/{num}/text_image.png", repeat=repeat
    )

    gif.add_image_fragment(text_image, repeat=repeat)

    # add_gif_fragment
    with GIF(
        save_path=f"tests/tests_data/test_GIF/{num}/gif1.gif",
        progress_bar=False,
    ) as temp_gif:
        temp_gif.add_text_fragment("gif 1")

    gif.add_gif_fragment(
        f"tests/tests_data/test_GIF/{num}/gif1.gif",
        duration=20,
        repeat=repeat,
    )

    with BytesIO() as temp_file:
        with GIF(save_path=temp_file, progress_bar=False) as temp_gif:
            temp_gif.add_text_fragment("gif 2", repeat=repeat)

        temp_file.seek(0)
        gif.add_gif_fragment(temp_file, duration=20, repeat=repeat)

    # gif.save(f"tests/result_images/test_GIF/{num}/test_GIF_{num}.gif")
    assert compare_gif(gif, f"tests/result_images/test_GIF/{num}/test_GIF_{num}.gif")


def test_extract_gif():
    assert (
        len(
            list(
                GIF.extract_gif_frames("tests/result_images/test_GIF/1/test_GIF_1.gif")
            )
        )
        == 645
    )
    assert (
        len(
            list(
                GIF.extract_gif_frames(
                    "tests/result_images/test_GIF/1/test_GIF_1.gif", speed=2
                )
            )
        )
        == 323
    )


def test_open():
    gif = GIF.open(
        "tests/result_images/test_GIF/1/test_GIF_1.gif",
        progress_bar=False,
    )
    assert compare_gif(gif, "tests/result_images/test_GIF/1/test_GIF_1.gif")
