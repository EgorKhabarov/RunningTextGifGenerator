from gif import GIF


gif = GIF()
gif.add_text_fragment("text", intro=True, outro=True, font_path="../fonts/Monocraft.otf")
gif.save(path="text.gif")
