import time
import itertools
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Callable, Generator, Any, Literal

from PIL import Image, ImageDraw, ImageFont


color_config = {
    "color_border": "#000000",
    "color_background": "#222222",
    "color_glare": "#666666",
    "color_pixel_off_light": "#880000",
    "color_pixel_off_dark": "#660000",
    "color_pixel_on_light": "#FF6666",
    "color_pixel_on_dark": "#FF0000",
}


def __print_progress_bar__(x: int, y: int, name: str, start: float):
    bar_length = 50

    if y == 0:
        y = 100

    arrow = ("█" * int(x / y * bar_length))[:bar_length]
    of_len = len(str(y))

    print(
        f"\r[{arrow:<{bar_length}}][{x:>{of_len}}/{y:>{of_len}} frames]"
        f"[{int(x / y * 100):>3}%][{time.perf_counter() - start:>5.2f}s][{name}]",
        end="\n" if x == y else "",
        flush=True,
    )


print_progress_bar = __print_progress_bar__


class GIF:
    color_config: dict[str, str] = color_config
    default_font_path: str = "./fonts/Monocraft.otf"
    __debug_path: str = "debug_image_frame_{fragment_index}.png"

    def __init__(
        self,
        columns: int = 79,
        rows: int = 9,
        *,
        default_font_path: str | Path | None = None,
        save_path: (
            str | bytes | PathLike[str] | PathLike[bytes] | BytesIO | None
        ) = None,
        loop: int = 0,
        debug: bool = False,
        debug_path: str | Path | None = None,
        progress_bar: bool = True,
    ):
        if columns < 1:
            raise ValueError("Minimum width = 1")
        if rows < 1:
            raise ValueError("Minimum height = 1")
        if loop < 0:
            raise ValueError("loop must be greater than or equal to 0")

        self.columns = columns
        self.rows = rows
        if default_font_path is not None:
            self.default_font_path = str(default_font_path)
        self.save_path = save_path
        self.loop = loop
        self.debug = debug
        if debug_path is not None:
            self.debug_path = debug_path
        self.progress_bar = progress_bar
        self.__fragments: list[
            tuple[
                Generator[Image.Image, Any, None] | list[Image.Image],
                Generator[int, Any, None] | list[int],
                int,
            ]
        ] = []

    def __enter__(self):
        if not self.save_path:
            raise ValueError(
                "When using the context manager, you need to specify save_path"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    @property
    def debug_path(self):
        return self.__debug_path

    @debug_path.setter
    def debug_path(self, debug_path: str | Path):
        debug_path_path = Path(debug_path)
        if debug_path_path.is_dir():
            raise ValueError("The debug_path must point to a file")
        debug_path_path.parent.mkdir(parents=True, exist_ok=True)
        self.__debug_path = str(debug_path)

    @property
    def columns_pixels(self):
        return self.columns * 2 + self.columns + 2 + 5 + 6

    @property
    def rows_pixels(self):
        return self.rows * 2 + self.rows + 3 + 5 + 5

    def generate_frame(
        self,
        func: Callable[[int, int], bool] = lambda c, r: False,
    ) -> Image.Image:
        """

        ┌─border──────────────────────────┐
        │ ┌─background──────────────────┐ │
        │ │  •pixels••••••─columns─•• │ │ │
        │ │  •••••••••••••••••••••••• │ │ │
        │ │  │row•••••••••••••••••••• │ │ │
        │ │  •••••••••••••••••••••••• │ │ │
        │ │ ─glare────────────────────┘ │ │
        │ └─────────────────────────────┘ │
        └─────────────────────────────────┘

        :param func: (column, row) -> is_on: bool
        :return:
        """
        columns_pixels = self.columns_pixels
        rows_pixels = self.rows_pixels

        image = Image.new("RGBA", (columns_pixels, rows_pixels), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # border
        draw.rounded_rectangle(
            (0, 0, columns_pixels - 1, rows_pixels - 1),
            radius=7,
            fill=color_config["color_border"],
        )
        # background
        draw.rectangle(
            (5, 5, columns_pixels - 6, rows_pixels - 6),
            color_config["color_background"],
        )
        # glare
        draw.line(
            (6, rows_pixels - 6, columns_pixels - 7, rows_pixels - 6),
            color_config["color_glare"],
        )
        draw.line(
            (columns_pixels - 6, 6, columns_pixels - 6, rows_pixels - 7),
            color_config["color_glare"],
        )

        # pixels
        for column in range(self.columns):
            for row in range(self.rows):
                is_on = func(column, row)
                start_pixel_column = 8 + (column * 2) + column - 1
                start_pixel_row = 8 + (row * 2) + row - 1
                string_is_on = "on" if is_on else "off"
                color_dark_pixel = self.color_config[f"color_pixel_{string_is_on}_dark"]
                color_light_pixel = self.color_config[
                    f"color_pixel_{string_is_on}_light"
                ]
                draw.rectangle(
                    (
                        start_pixel_column,
                        start_pixel_row,
                        start_pixel_column + 1,
                        start_pixel_row + 1,
                    ),
                    color_dark_pixel,
                )
                draw.point(
                    (start_pixel_column, start_pixel_row),
                    color_light_pixel,
                )
        return image

    def generate_text_image(
        self, text: str, font_path: str | BytesIO | None = None
    ) -> Image.Image:
        now_fragment_index = len(self.__fragments) + 1
        font_path = self.default_font_path if font_path is None else font_path
        font = ImageFont.truetype(font_path, 54)
        temp_img_cols, temp_img_rows = (
            int(font.getbbox(text)[2]) - 6,
            54 * (self.rows // 9) - 1,
        )

        # Temporary image with text
        temp_text_img = Image.new(
            mode="RGB",
            size=(temp_img_cols, temp_img_rows),
            color="#FFFFFF",
        )
        draw_text = ImageDraw.Draw(im=temp_text_img)
        draw_text.text(xy=(0, 0), text=text, fill="#000000", font=font)

        if self.debug:
            temp_text_img.save(
                self.debug_path.format(fragment_index=now_fragment_index)
            )

        text_cols = temp_img_cols * self.rows // temp_img_rows
        img_cols = text_cols

        img_rows = self.rows

        text_img = Image.new(
            mode="RGB",
            size=(img_cols, img_rows),
            color="#FFFFFF",
        )
        draw_text_resized = ImageDraw.Draw(im=text_img)

        if self.debug:
            text_img.save(self.debug_path.format(fragment_index=now_fragment_index))

        for resized_column_pixel in range(text_cols):
            for resized_row_pixel in range(img_rows):
                column_pixel = resized_column_pixel * 6 + 3
                row_pixel = resized_row_pixel * 6 + 3
                if temp_img_cols < column_pixel or temp_img_rows < row_pixel:
                    continue
                image_text_pixel = temp_text_img.getpixel((column_pixel, row_pixel))
                image_text_resized_pixel = (
                    (255, 255, 255)
                    if image_text_pixel == (255, 255, 255)
                    else (0, 0, 0)
                )
                draw_text_resized.point(
                    xy=(resized_column_pixel, resized_row_pixel),
                    fill=image_text_resized_pixel,
                )

        if self.debug:
            text_img.save(self.debug_path.format(fragment_index=now_fragment_index))

        return text_img

    def process_text_image(
        self,
        text_image: Image.Image,
        intro: bool = True,
        outro: bool = True,
        direction: str | Literal["left", "right", "up", "down", "none"] = "left",
    ) -> Image.Image:
        """

        :param text_image:
        :param intro:
        :param outro:
        :param direction:
        :return:
        """
        direction = direction.lower()
        if direction not in ("left", "right", "up", "down", "none"):
            raise ValueError(
                f'direction can only be one of "left", "right", '
                f'"up", "down", or "none". Not "{direction}".'
            )
        now_fragment_index = len(self.__fragments) + 1
        text_cols, text_rows = text_image.size
        new_image_cols, new_image_rows = text_cols, text_rows
        paste_col, paste_row = 0, 0

        match direction:
            case "left":
                if intro:
                    new_image_cols += self.columns
                    paste_col += self.columns
                if outro:
                    new_image_cols += self.columns
                elif text_cols < self.columns:
                    new_image_cols += self.columns - text_cols
            case "right":
                if intro:
                    new_image_cols += self.columns
                elif text_cols < self.columns:
                    new_image_cols += self.columns - text_cols

                if outro:
                    new_image_cols += self.columns
                    paste_col += self.columns
                elif text_cols < self.columns:
                    new_image_cols += self.columns - text_cols
                    paste_col += self.columns - text_cols
            case "up":
                if new_image_cols < self.columns:
                    new_image_cols = self.columns
                if intro:
                    new_image_rows += self.rows
                    paste_row += self.rows
                if outro:
                    new_image_rows += self.rows
            case "down":
                if new_image_cols < self.columns:
                    new_image_cols = self.columns
                if intro:
                    new_image_rows += self.rows
                if outro:
                    new_image_rows += self.rows
                    paste_row += self.rows

        if new_image_cols < self.columns:
            new_image_cols = self.columns
        if new_image_rows < self.rows:
            new_image_rows = self.rows

        image = Image.new(
            mode="RGB",
            size=(new_image_cols, new_image_rows),
            color="#FFFFFF",
        )
        image.paste(text_image, (paste_col, paste_row))
        if self.debug:
            image.save(self.debug_path.format(fragment_index=now_fragment_index))
        return image

    @staticmethod
    def extract_gif_frames(
        gif_file: Image.Image | BytesIO | str,
        speed: int = 1,
    ) -> Generator[tuple[Image.Image, int], Any, None]:
        frame_index = 0

        gif: Image.Image

        if isinstance(gif_file, (str, BytesIO)):
            gif = Image.open(gif_file)
        elif isinstance(gif_file, Image.Image):
            gif = gif_file
        else:
            raise ValueError("Wrong type")

        while True:
            if frame_index % speed != 0:
                frame_index += 1
                continue
            try:
                gif.seek(frame_index)
                yield gif.copy(), gif.info.get("duration", 0)
            except EOFError:
                break
            frame_index += 1

    def add_image_fragment(
        self,
        image_path: Image.Image | str,
        *,
        duration: int = 20,
        speed: int = 1,
        direction: str | Literal["left", "right", "up", "down", "none"] = "left",
        repeat: int = 1,
    ):
        """

        :param image_path:
        :param duration:
        :param speed:
        :param direction:
        :param repeat:
        :return:
        """
        direction = direction.lower()
        if direction not in ("left", "right", "up", "down", "none"):
            raise ValueError(
                f'direction can only be one of "left", "right", '
                f'"up", "down", or "none". Not "{direction}".'
            )

        if repeat < 1:
            raise ValueError("repeat must be greater than or equal to 1")

        image: Image.Image

        if isinstance(image_path, str):
            image = Image.open(image_path)
        elif isinstance(image_path, Image.Image):
            image = image_path
        else:
            raise ValueError("Wrong type")

        columns, rows = image.size
        if (columns, rows) < (self.columns, self.rows):
            raise ValueError(
                f"The size of this image does not match the size of the current gif "
                f"({columns}, {rows}) != ({self.columns_pixels}, {self.rows_pixels})"
                f"{image}"
            )

        if direction in ("left", "right"):
            count = columns - self.columns or 1
        elif direction in ("up", "down"):
            count = rows - self.rows or 1
        else:
            count = 1

        def check_pixel(n: int):
            match direction:
                case "left":
                    start_col, start_row = n, 0
                case "right":
                    start_col, start_row = -(n + self.columns - columns), 0
                case "up":
                    start_col, start_row = 0, n
                case "down":
                    start_col, start_row = 0, -(n + self.rows - rows)
                case _:
                    start_col, start_row = 0, 0

            def func(c: int, r: int) -> bool:
                try:
                    c += start_col
                    r += start_row
                    if c < 0 or r < 0:
                        return False
                    pixel = image.getpixel((c, r))
                    if not pixel or isinstance(pixel, float):
                        return False
                    return pixel[:3] == (0, 0, 0)
                except IndexError:
                    return False

            return func

        frames_count = len(range(0, count, speed))
        frames = (
            frame
            for generator in itertools.tee(
                (self.generate_frame(func=check_pixel(n)) for n in range(frames_count)),
                repeat,
            )
            for frame in generator
        )

        durations = (duration for _ in range(repeat) for _ in range(frames_count))
        self.__fragments.append((frames, durations, frames_count * repeat))
        return len(self.__fragments)

    def add_text_fragment(
        self,
        text: str,
        *,
        font_path: str | BytesIO | None = None,
        duration: int = 20,
        speed: int = 1,
        intro: bool = True,
        outro: bool = True,
        direction: str | Literal["left", "right", "up", "down", "none"] = "left",
        repeat: int = 1,
    ) -> int:
        """

        :param text:
        :param duration:
        :param speed:
        :param font_path:
        :param intro:
        :param outro:
        :param direction:
        :param repeat:
        :return: Fragment index
        """
        direction = direction.lower()
        if direction not in ("left", "right", "up", "down", "none"):
            raise ValueError(
                f'direction can only be one of "left", "right", '
                f'"up", "down", or "none". Not "{direction}".'
            )

        if repeat < 1:
            raise ValueError("repeat must be greater than or equal to 1")

        text_img = self.generate_text_image(text, font_path)
        image = self.process_text_image(text_img, intro, outro, direction)
        return self.add_image_fragment(
            image,
            duration=duration,
            speed=speed,
            direction=direction,
            repeat=repeat,
        )

    def add_gif_fragment(
        self,
        gif_path: Image.Image | BytesIO | str,
        *,
        duration: int | None = None,
        speed: int = 1,
        repeat: int = 1,
    ) -> int:
        """

        :param gif_path:
        :param duration:
        :param speed:
        :param repeat:
        :return:
        """
        if repeat < 1:
            raise ValueError("repeat must be greater than or equal to 1")

        gif_file: Image.Image

        if isinstance(gif_path, (str, BytesIO)):
            gif_file = Image.open(gif_path)
        elif isinstance(gif_path, Image.Image):
            gif_file = gif_path
        else:
            raise ValueError("Wrong type")

        now_fragment_index = len(self.__fragments) + 1

        columns, rows = gif_file.size
        if (columns, rows) != (self.columns_pixels, self.rows_pixels):
            raise ValueError(
                f"The size of this gif does not match the size of the current gif "
                f"({columns}, {rows}) != ({self.columns_pixels}, {self.rows_pixels})"
                f"{gif_file}"
            )

        frames = []
        durations_list = []
        for frame, duration_ in self.extract_gif_frames(gif_file, speed):
            frames.append(frame)
            durations_list.append(duration_)

        frames *= repeat
        durations_list *= repeat

        frames_count = len(frames)
        if duration is not None:
            durations = (duration for _ in range(frames_count))
        else:
            durations = (duration for duration in durations_list)

        self.__fragments.append((frames, durations, frames_count))
        return now_fragment_index

    def clear_fragments(self) -> None:
        self.__fragments.clear()

    def remove_fragment(self, index: int) -> None:
        self.__fragments.pop(index)

    def save(
        self,
        path: str | bytes | PathLike[str] | PathLike[bytes] | BytesIO | None = None,
        loop: int | None = None,
    ) -> None:
        """
        Creates a looping GIF from a list of images.

        :param path: Path or file for GIF
        :param loop:
        """
        if not self.__fragments:
            raise ValueError("You have not added any fragments")

        save_path = self.save_path if path is None else path
        if save_path is None:
            raise ValueError("save_path should not be None")

        loop = (self.loop if loop is None else loop) or 0
        if loop < 0:
            raise ValueError("loop must be greater than or equal to 0")

        frames: Generator[Image.Image, Any, None] = (
            frame for fragment in self.__fragments for frame in fragment[0]
        )
        durations: list[int] = list(
            duration for fragment in self.__fragments for duration in fragment[1]
        )
        count = sum(fragment[2] for fragment in self.__fragments)

        if not count:
            raise ValueError("You have not added any fragments")

        name: str = (
            save_path
            if isinstance(save_path, str)
            else getattr(save_path, "name", str(save_path))
        )
        start = time.perf_counter()
        if self.progress_bar:
            frames = (
                print_progress_bar(n, count, name, start) or frame
                for n, frame in enumerate(frames, start=0)
            )

        next(frames).save(
            fp=save_path,
            format="gif",
            save_all=True,
            append_images=frames,
            duration=durations,
            loop=loop,
        )
        if self.progress_bar:
            print_progress_bar(count, count, name, start)
        self.clear_fragments()
