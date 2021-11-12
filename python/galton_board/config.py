"""
This variables and constants are using in
the main file - main.py. Each section
is dived by following comment.
"""

from math import ceil
from pygame import init, display, FULLSCREEN

# display
init()

display_info = display.Info()
width = display_info.current_w
height = display_info.current_h
screen_mode = FULLSCREEN

FPS = 600

# instruments
instruments = {
    1: "balls",
    2: "walls",
}

# objects
walls_width = height // 200

parameters = {  #
    "elasticity": 0.1,
    "friction": 1.0,
    "walls_elasticity": 0.8,
    "gravity": (0, 300),
}

cparameters = {
    "amount": 10,
    "mass": 10,
    "radius": ceil(width * 0.01),
}

walls_coord = {
    "left": [(0, 0), (0, height)],
    "right": [(width, 0), (width, height)],
    "bottom": [(0, height), (width, height)],
    "top": [(0, 0), (width, 0)],
}

# widgets
sliders_type = {
    "elasticity:": {
        "min": 0.1,
        "max": 5,
        "step": 0.5,
        "initial": 0.1,
    },
    "friction:": {
        "min": 1.0,
        "max": 10.0,
        "step": 1,
        "initial": 1.0,
    },
    "wall_elasticity": {"min": 0.8, "max": 13, "step": 0.2, "initial": 0.8},
    "gravity": {"min": -2000, "max": 2000, "step": 200, "initial": 500}
}

handle_radius = ceil(width * 0.005)

# color
background_color = (0, 0, 0)
walls_color = (128, 128, 128, 255)

slider_color = (40, 40, 40)
slider_handler_color = (200, 200, 200)
text_color = (128, 128, 128)
