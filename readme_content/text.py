from gif import GIF


gif = GIF()
gif.default_font_path = "../fonts/Monocraft.otf"
gif.add_text_fragment("text", intro=True, outro=True)
gif.save(path="text.gif")
