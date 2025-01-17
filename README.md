
# GIF generator with a running text line

```shell
pip install -r requirements.txt
```

```python
from gif import GIF
gif = GIF()
gif.add_text_fragment("text", intro=True, outro=True)
gif.save(path="text.gif")
```
![text.gif](readme_content/text.gif)

You can specify the width and height of the screen.
By default they are `GIF(columns: int = 79, rows: int = 1)`.

### add_text_fragment

You can add a text fragment to a gif animation using the `add_text_fragment` method.
This method returns the index of the added fragment.

| Parameter                                                           | Description                                                                                                   |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| text: str                                                           | The text for the fragment                                                                                     |
| duration: int = 20                                                  | The speed of each frame within this fragment in milliseconds                                                  |
| speed: int = 1                                                      | Allows you to adjust the speed by selecting every x frame.<br>For example, `speed=2` takes every second frame |
| font_path: str &vert; BytesIO = "Monocraft.otf"                     | The path to the font. A pixel font with 9 pixel height letters                                                |
| intro: bool = False                                                 | Whether to fade the text onto the screen                                                                      |
| outro: bool = False                                                 | Whether to fade the text off the screen                                                                       |
| direction: Literal\["left", "right", "up", "down", "none"] = "left" | The direction of the text movement                                                                            |

### add_gif_fragment

You can add a fragment of a GIF file using the `add_gif_fragment` method.
This method returns the index of the added fragment.

| Parameter                                                           | Description                                                                                                   |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| gif_path: GifImagePlugin.GifImageFile &vert; str                    | Gif file or path to it<br/>`Image.open(gif_path)`                                                             |
| duration: int = ...                                                 | The speed of gif fragment in milliseconds<br/>By default, the gif speed is taken                              |
| speed: int = 1                                                      | Allows you to adjust the speed by selecting every x frame.<br>For example, `speed=2` takes every second frame |

### remove_fragment
Deletes a fragment by index.

### clear_fragments
Removes all fragments.

### save
Saves a gif to a path or file `path: str | BytesIO`.
Calls `clear_fragments` after saving.

The font can be downloaded [here](https://fonts-online.ru/fonts/monocraft)
