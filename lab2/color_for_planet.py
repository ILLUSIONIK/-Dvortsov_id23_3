def color_name_to_rgb(color_name):
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "gray": (128, 128, 128),
        "darkgray": (169, 169, 169),
        "lightblue": (173, 216, 230),
        "silver": (192, 192, 192),
        "lightgray": (211, 211, 211)
    }
    return colors.get(color_name, (255, 255, 255))
def density_to_color(density, color):
        base_color = color_name_to_rgb(color)
        brightness = 255 - int(density)
        brightness = max(0, min(brightness, 255))
        return f'#{brightness & 255:02x}{base_color[1]:02x}{base_color[2]:02x}'
