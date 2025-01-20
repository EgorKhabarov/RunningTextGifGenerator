from gif import GIF
from tests.utils import ExceptionWrapper, compare_gif


def test_utils():
    with ExceptionWrapper(
        Exception("Expected exception ValueError('error') was not raised")
    ):
        with ExceptionWrapper(ValueError("error")):
            pass

    with ExceptionWrapper(Exception("ValueError('error') != ValueError('exception')")):
        with ExceptionWrapper(ValueError("error")):
            raise ValueError("exception")

    assert (
        compare_gif(
            GIF.open(
                "tests/result_images/test_direction/1/test_direction_1_True_True.gif",
                progress_bar=False,
            ),
            "tests/result_images/test_direction/2/test_direction_2_True_False.gif",
        )
        is False
    )

    gif1 = GIF(progress_bar=False)
    gif1.add_text_fragment("text", outro=False)

    gif2 = GIF(progress_bar=False)
    gif2.add_text_fragment("text", outro=True)
    gif2.save("tests/result_images/test_utils/1/test_utils_1.gif")

    assert (
        compare_gif(
            gif1,
            "tests/result_images/test_utils/1/test_utils_1.gif",
        )
        is False
    )
