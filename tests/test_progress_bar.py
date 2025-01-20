import re
import sys
from io import StringIO, BytesIO

from gif import GIF


def test_progress_bar():
    gif = GIF(6)
    gif.add_text_fragment("12", intro=False, outro=False)
    sys.stdout = StringIO()
    file = BytesIO()
    gif.save(file)
    sys.stdout.seek(0)

    def replace_time(text: str):
        return re.sub(r"\[[\d ]\d\.\d{2}s]", "[ 0:00s]", text)

    test_output = replace_time(sys.stdout.read().strip()).splitlines()
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
    sys.stdout = sys.__stdout__
    assert test_output == output
