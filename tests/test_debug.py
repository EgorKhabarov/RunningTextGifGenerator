from pathlib import Path

from gif import GIF


def test_debug():
    gif = GIF(
        rows=10,
        debug=True,
        debug_path=Path(
            "tests",
            "debug_images",
            "test_debug",
            "1",
            "test_debug_1_{fragment_index}.png",
        ),
        progress_bar=False,
    )
    gif.add_text_fragment("1", intro=False, outro=False, direction="none")
    assert Path(
        "tests",
        "debug_images",
        "test_debug",
        "1",
        "test_debug_1_1.png",
    ).exists()
