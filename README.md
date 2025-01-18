
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
| font_path: str \| BytesIO \| None = None                            | The path to the font. A pixel font with 9 pixel height letters                                                |
| duration: int = 20                                                  | The speed of each frame within this fragment in milliseconds                                                  |
| speed: int = 1                                                      | Allows you to adjust the speed by selecting every x frame.<br>For example, `speed=2` takes every second frame |
| intro: bool = True                                                  | Whether to fade the text onto the screen                                                                      |
| outro: bool = True                                                  | Whether to fade the text off the screen                                                                       |
| direction: Literal\["left", "right", "up", "down", "none"] = "left" | The direction of the text movement                                                                            |

### add_image_fragment

You can add a image fragment to a gif animation using the `add_image_fragment` method.
This method returns the index of the added fragment.

| Parameter                      | Description                                                                                                   |
|--------------------------------|---------------------------------------------------------------------------------------------------------------|
| image_path: Image.Image \| str | Image file or path to it<br/>`Image.open(image_path)`                                                         |
| duration: int = 20             | The speed of each frame within this fragment in milliseconds                                                  |
| speed: int = 1                 | Allows you to adjust the speed by selecting every x frame.<br>For example, `speed=2` takes every second frame |

#### Example

<table><tbody>
<tr><td rowspan="2">

```python
from gif import GIF


gif = GIF(columns=22, rows=24)
gif.add_image_fragment(
    image_path="dino.png",
    direction="up",
    duration=100,
    speed=24,
)
gif.save(path="dino.gif")

```
</td><td>

`dino.png`
</td><td>

`dino.gif`
</td></tr>
<tr>
<td><img alt="dino.png" src="readme_content/dino.png" width="50" style="image-rendering: pixelated;"></td>
<td><img alt="dino.gif" src="readme_content/dino.gif"></td>
</tr></tbody></table>


### add_gif_fragment

You can add a fragment of a GIF file using the `add_gif_fragment` method.
This method returns the index of the added fragment.

| Parameter                               | Description                                                                                                   |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------|
| gif_path: Image.Image \| BytesIO \| str | Gif file or path to it<br/>`Image.open(gif_path)`                                                             |
| duration: int \| None = None            | The speed of gif fragment in milliseconds<br/>By default, the gif speed is taken                              |
| speed: int = 1                          | Allows you to adjust the speed by selecting every x frame.<br>For example, `speed=2` takes every second frame |

### remove_fragment
Deletes a fragment by index.

### clear_fragments
Removes all fragments.

### save
Saves a gif to a path or file `path: str | BytesIO`.
Calls `clear_fragments` after saving.

The font can be downloaded [here](https://fonts-online.ru/fonts/monocraft)
