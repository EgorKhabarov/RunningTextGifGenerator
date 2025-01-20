from PIL import Image

from gif import GIF
from tests.utils import ExceptionWrapper


def test_exceptions():
    with ExceptionWrapper(ValueError("Minimum width = 1")):
        GIF(columns=0)

    with ExceptionWrapper(ValueError("Minimum height = 1")):
        GIF(rows=0)

    with ExceptionWrapper(
        ValueError("When using the context manager, you need to specify save_path")
    ):
        with GIF():
            pass

    with ExceptionWrapper(ValueError("You have not added any fragments.")):
        with GIF(save_path="path"):
            pass

    with ExceptionWrapper(ValueError("The debug_path must point to a file")):
        GIF().debug_path = "tests/debug_images/"

    with ExceptionWrapper(
        ValueError(
            f'direction can only be one of "left", "right", "up", "down", or "none". Not "lorem ipsum".'
        )
    ):
        GIF().add_text_fragment("text", direction="Lorem ipsum")

    with ExceptionWrapper(
        ValueError(
            f'direction can only be one of "left", "right", "up", "down", or "none". Not "lorem ipsum".'
        )
    ):
        GIF().add_image_fragment(Image.new("RGB", (1, 1)), direction="Lorem ipsum")

    with ExceptionWrapper(ValueError(f"Wrong type")):
        GIF().add_image_fragment(None)  # type: ignore

    with ExceptionWrapper(ValueError(f"Wrong type")):
        GIF().add_gif_fragment(None)  # type: ignore

    test_image = Image.new("RGB", (78, 8))
    test_gif = GIF(columns=79, rows=9)
    with ExceptionWrapper(
        ValueError(
            "The size of this image does not match the size of the current gif "
            "(78, 8) != ({columns_pixels}, {rows_pixels})"
            "{test_image}".format(
                test_image=test_image,
                columns_pixels=test_gif.columns_pixels,
                rows_pixels=test_gif.rows_pixels,
            )
        )
    ):
        test_gif.add_image_fragment(test_image)
