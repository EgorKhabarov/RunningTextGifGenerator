# noinspection PyPackageRequirements
import pytest

from gif import GIF
from tests.utils import compare_gif


@pytest.mark.parametrize(
    "num, intro, outro, durations",
    (
        (1, True, True, (50, 66, 200, 66, 200, 50, 200, 50, 200, 1000)),
        (2, True, False, (50, 66, 200, 66, 200, 50, 200, 50, 200, 1000)),
        (3, False, True, (50, 66, 200, 66, 200, 50, 200, 50, 200, 1000)),
        (4, False, False, (50, 1000, 1000, 66, 1000, 50, 1000, 50, 1000, 1000)),
    ),
)
def test_direction(num: int, intro: bool, outro: bool, durations: tuple[int]):
    gif = GIF(debug=False, progress_bar=False)

    gif.debug_path = (
        f"tests/debug_images/test_direction/{num}/"
        f"test_direction_{num}_{intro}_{outro}_{{fragment_index}}.png"
    )

    gif.add_text_fragment(f"--{intro=};{outro=}--", intro=False, outro=False, direction="left", duration=durations[0])
    gif.add_text_fragment("left", intro=intro, outro=outro, direction="left", duration=durations[1])
    gif.add_text_fragment("up", intro=intro, outro=outro, direction="up", duration=durations[2])
    gif.add_text_fragment("right", intro=intro, outro=outro, direction="right", duration=durations[3])
    gif.add_text_fragment("down", intro=intro, outro=outro, direction="down", duration=durations[4])
    gif.add_text_fragment("left biiiiiig teeexxxt", intro=intro, outro=outro, direction="left", duration=durations[5])
    gif.add_text_fragment("up biiiiiig teeexxxt", intro=intro, outro=outro, direction="up", duration=durations[6])
    gif.add_text_fragment("right biiiiiig teeexxxt", intro=intro, outro=outro, direction="right", duration=durations[7])
    gif.add_text_fragment("down biiiiiig teeexxxt", intro=intro, outro=outro, direction="down", duration=durations[8])
    gif.add_text_fragment("None", intro=intro, outro=outro, direction="none", duration=durations[9])

    path = f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif"
    # gif.save(path)
    assert compare_gif(gif, path)
