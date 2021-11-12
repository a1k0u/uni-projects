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

FPS = 600

# instruments
instruments = {
    1: "balls",
    2: "walls",
}

# objects
gravity = 0, height * 3  #

walls_elasticity = 0.8  #
walls_width = height // 100

ball_parameters = {  #
    "amount": 10,
    "mass": 10,
    "radius": ceil(width * 0.005),
    "elasticity": 0.1,
    "friction": 1.0,
}

walls_coord = {
    "left": [(0, 0), (0, height)],
    "right": [(width, 0), (width, height)],
    "bottom": [(0, height), (width, height)],
    "top": [(0, 0), (width, 0)]
}

# color
background_color = (0, 0, 0)
walls_color = (128, 128, 128, 255)
