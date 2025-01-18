from gif import GIF


gif = GIF()
gif.default_font_path = "../fonts/Monocraft.otf"
gif.add_text_fragment("this is text.gif:")
gif.add_gif_fragment(gif_path="text.gif")
gif.save(path="text_text.gif")
