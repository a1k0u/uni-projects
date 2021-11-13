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
            x=ceil(c.width * 0.825),
            y=ceil(c.height * 0.1 * i + c.height * 0.1),
            width=c.width // 8,
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


def create_text_widgets(surface: Surface) -> None:
    return [
        TextBox(
            surface,
            x=ceil(c.width * 0.825),
            y=ceil(c.height * 0.1 * i + c.height * 0.1),
            width=0,
            height=0,
            fontSize=ceil(c.width * 0.015),
            textColour=c.text_color,
        )
        for i in range(len(c.text_widget))
    ]
