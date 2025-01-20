import re

# noinspection PyPackageRequirements
import pytest
from io import StringIO, BytesIO
from contextlib import redirect_stdout

from gif import GIF


@pytest.mark.parametrize(
    "loop, repeat",
    [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
    ],
)
def test_progress_bar(loop: int, repeat: int):
    def replace_time(text: str):
        return re.sub(r"\[[\d ]\d\.\d{2}s]", "[ 0:00s]", text)

    stdout_file = StringIO()
    file = BytesIO()

    gif = GIF(6, loop=loop)
    gif.add_text_fragment("12", intro=False, outro=False, repeat=repeat)

    with redirect_stdout(stdout_file):
        gif.save(file)

    stdout_file.seek(0)
    test_output = replace_time(stdout_file.read().strip()).splitlines()
    if repeat == 1:
        output = replace_time(
            f"""
[                                                  ][0/5 frames][  0%][ 0.00s][{file}]
[██████████                                        ][1/5 frames][ 20%][ 0.00s][{file}]
[████████████████████                              ][2/5 frames][ 40%][ 0.00s][{file}]
[██████████████████████████████                    ][3/5 frames][ 60%][ 0.00s][{file}]
[████████████████████████████████████████          ][4/5 frames][ 80%][ 0.00s][{file}]
[██████████████████████████████████████████████████][5/5 frames][100%][ 0.00s][{file}]
""".strip()
        ).splitlines()
    else:
        output = replace_time(
            f"""
[                                                  ][ 0/10 frames][  0%][ 0:00s][{file}]
[█████                                             ][ 1/10 frames][ 10%][ 0:00s][{file}]
[██████████                                        ][ 2/10 frames][ 20%][ 0:00s][{file}]
[███████████████                                   ][ 3/10 frames][ 30%][ 0:00s][{file}]
[████████████████████                              ][ 4/10 frames][ 40%][ 0:00s][{file}]
[█████████████████████████                         ][ 5/10 frames][ 50%][ 0:00s][{file}]
[██████████████████████████████                    ][ 6/10 frames][ 60%][ 0:00s][{file}]
[███████████████████████████████████               ][ 7/10 frames][ 70%][ 0:00s][{file}]
[████████████████████████████████████████          ][ 8/10 frames][ 80%][ 0:00s][{file}]
[█████████████████████████████████████████████     ][ 9/10 frames][ 90%][ 0:00s][{file}]
[██████████████████████████████████████████████████][10/10 frames][100%][ 0:00s][{file}]
""".strip()
        ).splitlines()
    assert test_output == output
