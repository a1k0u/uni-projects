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

menu_coord_x = ceil(width * 0.775)
menu_bar_x = menu_coord_x + 0.75 * walls_width
menu_bar_y = walls_width
menu_bar_width = width - menu_coord_x - 2 * walls_width
menu_bar_height = height - 2 * walls_width

menu_bar_draw = [menu_bar_x, menu_bar_y, menu_bar_width, menu_bar_height]
menu_bar_rect = [menu_bar_x, 0, width, height]

parameters = {
    "ball_amount": 10,
    "ball_mass": 10,
    "ball_radius": ceil(width * 0.01),
    "ball_elasticity": 0.1,
    "friction": 1.0,
    "walls_elasticity": 0.8,
    "gravity": (0, 300),
}

walls_coord = {
    "left": [(0, 0), (0, height), walls_width],
    "right": [(width, 0), (width, height), walls_width],
    "bottom": [(0, height), (width, height), walls_width],
    "top": [(0, 0), (width, 0), walls_width],
    "menu": [(menu_coord_x, 0), (menu_coord_x, height), walls_width // 2],
}

funnel_width = width - menu_bar_width
funnel_hole_width = ceil(funnel_width * 0.025)
funnel_hole_height = ceil(funnel_hole_width * 0.25)
funnel_height = ceil(height * 0.325)
funnel_coord_left = {
    "top": [
        (0, 0),
        (funnel_width // 2 - funnel_hole_width,
         funnel_height // 2 - funnel_hole_height),
        walls_width // 2,
    ],
    "vertical": [
        (funnel_width // 2 - funnel_hole_width,
         funnel_height // 2 - funnel_hole_height),
        (funnel_width // 2 - funnel_hole_width,
         funnel_height // 2 + funnel_hole_height),
        walls_width // 2,
    ],
    "bottom": [
        (funnel_width // 2 - funnel_hole_width,
         funnel_height // 2 + funnel_hole_height),
        (0, funnel_height),
        walls_width // 2,
    ]
}
funnel_coord_right = {
    "top": [
        (funnel_width, 0),
        (funnel_width // 2 + funnel_hole_width,
         funnel_height // 2 - funnel_hole_height),
        walls_width // 2,
    ],
    "vertical": [
        (funnel_width // 2 + funnel_hole_width,
         funnel_height // 2 - funnel_hole_height),
        (funnel_width // 2 + funnel_hole_width,
         funnel_height // 2 + funnel_hole_height),
        walls_width // 2,
    ],
    "bottom": [
        (funnel_width // 2 + funnel_hole_width,
         funnel_height // 2 + funnel_hole_height),
        (funnel_width, funnel_height),
        walls_width // 2,
    ]
}

# widgets
sliders_type = {
    "ball_amount": {"min": 1, "max": 20, "step": 2, "initial": 5},
    "ball_mass": {"min": 1, "max": 100, "step": 10, "initial": 5},
    "ball_radius": {"min": 10, "max": 100, "step": 10, "initial": 5},
    "ball_elasticity:": {
        "min": 0.1,
        "max": 5,
        "step": 0.5,
        "initial": 0.1,
    },
    "ball_friction:": {
        "min": 1.0,
        "max": 10.0,
        "step": 1,
        "initial": 1.0,
    },
    "wall_elasticity": {"min": 0.8, "max": 13, "step": 0.2, "initial": 0.8},
    "gravity": {"min": -5000, "max": 10000, "step": 300, "initial": 300},
}

text_widget = [
    "Amount of balls",
    "Value of ball's mass",
    "Value of ball's radius",
    "Value of ball's elasticity",
    "Value of ball's friction",
    "Value of wall's elasticity",
    "Value of gravity",
]
pos_x_text = ceil(width * 0.81725)
pos_x_slider = ceil(width * 0.825)
pos_y_step = height * 0.075

font_size = ceil(width * 0.015)
handle_radius = ceil(width * 0.005)
slider_width = width // 8

# color
background_color = (0, 0, 0)
walls_color = (128, 128, 128, 255)

slider_color = (40, 40, 40)
slider_handler_color = (200, 200, 200)
text_color = (128, 128, 128)
