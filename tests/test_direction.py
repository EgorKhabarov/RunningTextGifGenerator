from gif import GIF
from tests.utils import compare_gif


def test_direction():
    gif = GIF(debug=False, progress_bar=False)

    num = 1
    intro = True
    outro = True
    gif.debug_path = (
        f"tests/debug_images/test_direction/{num}/"
        f"test_direction_{num}_{intro}_{outro}_{{fragment_index}}.png"
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
    # gif.save(f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif")
    assert compare_gif(
        gif,
        f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif",
    )

    num = 2
    intro = True
    outro = False
    gif.debug_path = (
        f"tests/debug_images/test_direction/{num}/"
        f"test_direction_{num}_{intro}_{outro}_{{fragment_index}}.png"
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
    # gif.save(f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif")
    assert compare_gif(
        gif,
        f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif",
    )

    num = 3
    intro = False
    outro = True
    gif.debug_path = (
        f"tests/debug_images/test_direction/{num}/"
        f"test_direction_{num}_{intro}_{outro}_{{fragment_index}}.png"
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
    # gif.save(f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif")
    assert compare_gif(
        gif,
        f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif",
    )

    num = 4
    intro = False
    outro = False
    gif.debug_path = (
        f"tests/debug_images/test_direction/{num}/"
        f"test_direction_{num}_{intro}_{outro}_{{fragment_index}}.png"
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
    # gif.save(f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif")
    assert compare_gif(
        gif,
        f"tests/result_images/test_direction/{num}/test_direction_{num}_{intro}_{outro}.gif",
    )
