from math import ceil

from pygame import Surface
from pygame_widgets.slider import Slider

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
