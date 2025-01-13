import time
from io import BytesIO
from typing import Callable, Generator, Any, Literal

from PIL import Image, ImageDraw, ImageFont


color_border = "#000000"
color_background = "#222222"
color_glare = "#666666"
color_pixel_off_light = "#880000"
color_pixel_off_dark = "#660000"
color_pixel_on_light = "#FF6666"
color_pixel_on_dark = "#FF0000"


def print_progress_bar(x: int, y: int, name: str, start: float):
    bar_length = 50

    if y == 0:
        y = 100

    arrow = ("█" * int(x / y * bar_length))[:bar_length]

    print(
        f"\r[{arrow:<{bar_length}}][{x}/{y} frames]"
        f"[{int(x / y * 100):>3}%][{time.perf_counter() - start:>5.2f}s][{name}]",
        end="",
        flush=True,
    )


class GIF:
    def __init__(self, columns: int = 79, rows: int = 1, debug: bool = False):
        if columns < 6:
            raise ValueError("Minimum width = 6")
        if rows < 1:
            raise ValueError("Minimum height = 1")

        self.columns = columns
        self.rows = 9 * rows
        self.debug = debug
        self.__fragments: list[
            tuple[Generator[Image, Any, None], Generator[int, Any, None], int]
        ] = []

    def __generate_frame(
        self, func: Callable[[int, int], bool] = lambda c, r: False
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
        columns_pixels = self.columns * 2 + self.columns + 2 + 5 + 6
        rows_pixels = self.rows * 2 + self.rows + 3 + 5 + 5

        image = Image.new("RGBA", (columns_pixels, rows_pixels), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # border
        draw.rounded_rectangle(
            (0, 0, columns_pixels - 1, rows_pixels - 1), radius=7, fill=color_border
        )
        # background
        draw.rectangle((5, 5, columns_pixels - 6, rows_pixels - 6), color_background)
        # glare
        draw.line(
            (6, rows_pixels - 6, columns_pixels - 7, rows_pixels - 6), color_glare
        )
        draw.line(
            (columns_pixels - 6, 6, columns_pixels - 6, rows_pixels - 7), color_glare
        )

        # pixels
        for column in range(self.columns):
            for row in range(self.rows):
                is_on = func(column, row)
                start_pixel_column = 8 + (column * 2) + column - 1
                start_pixel_row = 8 + (row * 2) + row - 1
                draw.rectangle(
                    (
                        start_pixel_column,
                        start_pixel_row,
                        start_pixel_column + 1,
                        start_pixel_row + 1,
                    ),
                    color_pixel_on_dark if is_on else color_pixel_off_dark,
                )
                draw.point(
                    (start_pixel_column, start_pixel_row),
                    color_pixel_on_light if is_on else color_pixel_off_light,
                )
        return image

    def __generate_text_image(self, text: str, font_path: str | BytesIO) -> Image.Image:
        now_fragment_index = len(self.__fragments) + 1
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
            temp_text_img.save(f"temp_image_{now_fragment_index}.png", "png")

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
            text_img.save(f"temp_image_{now_fragment_index}.png", "png")

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
            text_img.save(f"temp_image_{now_fragment_index}.png", "png")

        return text_img

    def __process_text_image(
        self,
        text_image: Image.Image,
        intro: bool = False,
        outro: bool = False,
        direction: Literal["left", "right", "up", "down", "none"] = "left",
    ) -> Image.Image:
        now_fragment_index = len(self.__fragments) + 1
        text_cols, text_rows = text_image.size
        new_image_cols, new_image_rows = text_cols, text_rows
        if new_image_cols < self.columns and not (intro and outro):
            new_image_cols = self.columns
        if new_image_rows < self.rows and not (intro and outro):
            new_image_rows = self.rows
        paste_col, paste_row = 0, 0

        match direction:
            case "left":
                if intro:
                    new_image_cols += self.columns
                    paste_col += self.columns
                if outro:
                    new_image_cols += self.columns
            case "right":
                if intro:
                    new_image_cols += self.columns
                if outro:
                    new_image_cols += self.columns
                    paste_col += self.columns
                if not (intro and outro):
                    new_image_cols += self.columns - text_cols
                    paste_col += self.columns - text_cols
            case "up":
                if intro:
                    new_image_rows += self.rows
                    paste_row += self.rows
                if outro:
                    new_image_rows += self.rows
            case "down":
                if intro:
                    new_image_rows += self.rows
                if outro:
                    new_image_rows += self.rows
                    paste_row += self.rows
            case "none":
                if new_image_rows < self.columns:
                    new_image_rows = self.columns

        image = Image.new(
            mode="RGB",
            size=(new_image_cols, new_image_rows),
            color="#FFFFFF",
        )
        image.paste(text_image, (paste_col, paste_row))
        if self.debug:
            image.save(f"temp_image_{now_fragment_index}.png", "png")
        return image

    def add_fragment(
        self,
        text: str,
        *,
        duration: int = 20,
        speed: int = 1,
        font_path: str | BytesIO = "Monocraft.otf",
        intro: bool = False,
        outro: bool = False,
        direction: Literal["left", "right", "up", "down", "none"] = "left",
    ) -> int:
        """

        :param text:
        :param duration:
        :param speed:
        :param font_path:
        :param intro:
        :param outro:
        :param direction:
        :return: Fragment index
        """
        now_fragment_index = len(self.__fragments) + 1

        text_img = self.__generate_text_image(text, font_path)
        # text_cols, text_rows = text_img.size
        data = self.__process_text_image(text_img, intro, outro, direction)
        image_cols, image_rows = data.size

        if direction in ("left", "right"):
            count = image_cols - self.columns or 1
        elif direction in ("up", "down"):
            count = image_rows - self.rows or 1
        else:  # direction == "none"
            count = 1

        def check_pixel(n: int):
            match direction:
                case "left":
                    start_col, start_row = n, 0
                case "right":
                    start_col, start_row = -(n + self.columns - image_cols), 0
                case "up":
                    start_col, start_row = 0, n
                case "down":
                    start_col, start_row = 0, -(n + self.rows - image_rows)
                case _:  # "none"
                    start_col, start_row = 0, 0

            def _(c: int, r: int) -> bool:
                try:
                    c += start_col
                    r += start_row
                    if c < 0 or r < 0:
                        return False
                    return data.getpixel((c, r)) == (0, 0, 0)
                except IndexError:
                    return False

            return _

        frames = (
            self.__generate_frame(func=check_pixel(n)) for n in range(0, count, speed)
        )

        frames_count = len(range(0, count, speed))
        durations = (duration for _ in range(frames_count))
        self.__fragments.append((frames, durations, frames_count))
        return now_fragment_index

    def clear_fragments(self):
        self.__fragments.clear()

    def remove_fragment(self, index: int):
        self.__fragments.pop(index)

    def save(self, path: str | BytesIO):
        """
        Creates a looping GIF from a list of images.

        :param path: Path or file for GIF
        """
        if not self.__fragments:
            raise ValueError("You have not added any fragments.")

        frames: Generator[Image.Image, Any, None] = (
            frame for fragment in self.__fragments for frame in fragment[0]
        )
        durations: list[int] = list(
            duration for fragment in self.__fragments for duration in fragment[1]
        )
        count = sum(fragment[2] for fragment in self.__fragments)

        if not count:
            raise ValueError("You have not added any fragments.")

        name = path if isinstance(path, str) else path.name or path
        start = time.perf_counter()
        frames = (
            print_progress_bar(n, count, name, start) or i
            for n, i in enumerate(frames, 0)
        )

        next(frames).save(
            fp=path,
            save_all=True,
            append_images=frames,
            duration=durations,
            loop=0,
        )
        print_progress_bar(count, count, name, start)
