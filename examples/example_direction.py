from gif import GIF


gif = GIF()
arguments = {"text": "text", "intro": True, "outro": True, "font_path": "../Monocraft.otf"}
gif.add_fragment(**arguments, direction="left", duration=20)
gif.add_fragment(**arguments, direction="right", duration=20)
gif.add_fragment(**arguments, direction="up", duration=60)
gif.add_fragment(**arguments, direction="down", duration=60)
gif.save("example_direction.gif")
