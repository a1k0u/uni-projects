"""
This variables and constants are using in
the main file - main.py. Each section
is dived by following comment.
"""

from math import ceil
from pygame import init, display

# display
init()

display_info = display.Info()
width = display_info.current_w
height = display_info.current_h

CAPTION = ""

FPS = 600

parameters = {"points": width // 10, "colors": 3, "kNN": 3}
menu_height = ceil(height * 0.1)

# objects
point_radius = ceil(width * 0.005)
point_outline_radius = point_radius + ceil(width * 0.0015)
line_radius = ceil(point_radius * 0.3)
cursor_radius = ceil(point_radius * 0.5)
cursor_outline_radius = ceil(point_radius * 0.75)
pressed_button_radius = ceil(width * 0.001)

width_block = point_radius + ceil(width * 0.0075)
block_step = point_radius + ceil(width * 0.0088)

# color
MAKE_LIGHTER = 92
MAKE_DARKER = -92
MAKE_DARKER_64 = -64

black = (0, 0, 0)
orange = (255, 79, 0)
white = (255, 255, 255)
white_alpha_64 = (255, 255, 255, 64)
white_alpha_128 = (255, 255, 255, 128)

point_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (224, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]
background_color = (0, 0, 0)
menu_bar_color = (0, 0, 0)
outline_color = (0, 0, 0, 200)
cursor_color = (255, 255, 255)
outline_cursor_color = (0, 0, 0)

slider_color = (40, 40, 40)
slider_handler_color = (200, 200, 200)
text_color = (128, 128, 128)

# widgets
sliders_type = {
    "points:": {
        "min": 2,
        "max": parameters["points"],
        "step": 20,
        "initial": parameters["points"] // 4,
    },
    "colors:": {
        "min": 2,
        "max": len(point_colors),
        "step": 1,
        "initial": 2,
    },
    "kNN": {"min": 1, "max": 13, "step": 1, "initial": 3},
}

EDIT_MODE_TEXT = "Classify mode"
SPIDER_MODE_TEXT = "Spider mode"
SLIDERS_TEXT = "Amount of"
BUTTONS_TEXT = "Choose color:"
NON_BUTTONS_TEXT = ""
