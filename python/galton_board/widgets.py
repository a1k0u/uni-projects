from math import ceil

from pygame import Surface
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

import config as c


def create_slider_widgets(surface: Surface) -> list:
    """
    Returns list of sliders from pygame-widget.
    Parameters for each slider has been mentioned
    in config file.
    :param surface: Surface
    :return: list
    """
    return [
        Slider(
            surface,
            x=c.pos_x_slider,
            y=ceil(c.pos_y_step * i + c.pos_y_step),
            width=c.slider_width,
            height=c.handle_radius,
            min=c.sliders_type[key]["min"],
            max=c.sliders_type[key]["max"],
            step=c.sliders_type[key]["step"],
            initial=c.sliders_type[key]["initial"],
            colour=c.slider_color,
            handleRadius=c.handle_radius,
            handleColour=c.slider_handler_color,
        )
        for i, key in enumerate(c.sliders_type)
    ]


def create_text_widgets(surface: Surface) -> list:
    """
    Returns list of text boxes from pygame-widget.
    Parameters for each text box has been mentioned
    in config file.
    :param surface: Surface
    :return: list
    """
    return [
        TextBox(
            surface,
            x=c.pos_x_text,
            y=ceil(c.pos_y_step * i + c.pos_y_step),
            width=0,
            height=0,
            fontSize=c.font_size,
            textColour=c.text_color,
        )
        for i in range(len(c.text_widget))
    ]
