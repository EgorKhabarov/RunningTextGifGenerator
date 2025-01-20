from io import BytesIO
from pathlib import Path
from itertools import zip_longest

from PIL import Image

from gif import GIF


class ExceptionWrapper:
    def __init__(self, exception: Exception | type[Exception]):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise Exception(f"Expected exception {self.exception!r} was not raised")
        if (
            isinstance(exc_val, type(self.exception))
            and exc_val.args == self.exception.args
        ):
            return True
        raise Exception(f"{self.exception!r} != {exc_val!r}")


def compare_gif(gif: GIF, path: str | Path):
    test_file = BytesIO()
    gif.save(test_file)
    test_file.seek(0)
    test_gif = Image.open(test_file)

    result_gif = Image.open(path)

    test_frames = GIF.extract_gif_frames(test_gif)
    result_frames = GIF.extract_gif_frames(result_gif)
    for test_image, result_image in zip_longest(test_frames, result_frames):
        if None in (test_image, result_image):
            return False

        (test_image, _), (result_image, _) = test_image, result_image

        if test_image != result_image:
            return False
    return True
