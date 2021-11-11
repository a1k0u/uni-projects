from math import ceil

from pygame import Rect, Surface
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle

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
            x=ceil(c.width * 0.2 * i + c.width * 0.015),
            y=ceil(c.height * 0.053),
            width=c.width // 6,
            height=c.point_radius,
            min=c.sliders_type[key]["min"],
            max=c.sliders_type[key]["max"],
            step=c.sliders_type[key]["step"],
            initial=c.sliders_type[key]["initial"],
            colour=c.slider_color,
            handleRadius=c.point_radius,
            handleColour=c.slider_handler_color,
        )
        for i, key in enumerate(c.sliders_type)
    ]


def create_toggle_widget(surface: Surface) -> Toggle:
    """
    Returns Toggle from pygame-widget
    for changing mode in application.
    :param surface: Surface
    :return: Toggle
    """
    return Toggle(
        surface,
        x=ceil(c.width * 0.617),
        y=ceil(c.height * 0.053),
        width=ceil(c.width * 0.02),
        height=ceil(c.width * 0.005),
        handleRadius=c.point_radius,
        startOn=True,
        onColour=c.text_color,
        offColour=c.slider_color,
        handleOnColour=c.slider_handler_color,
        handleOffColour=c.slider_handler_color,
    )


def create_text_widgets(surface: Surface) -> list:
    """
    Returns list of pygame-widget components - Textbox.
    This text widgets are using for all pygame-widgets.
    :param surface: Surface
    :return: list
    """
    return [
        TextBox(
            surface,
            x=ceil(c.width * 0.2 * i + c.width * 0.008),
            y=ceil(c.height * 0.053),
            width=0,
            height=0,
            fontSize=ceil(c.width * 0.015),
            textColour=c.text_color,
        )
        for i in range(len(c.sliders_type) + 1)
    ]


def create_color_buttons(colors_amount: int) -> list:
    """
    Returns list of pygame objects - Rect.
    This buttons are using for choosing color.
    :param colors_amount: int
    :return: list
    """
    return [
        Rect(
            ceil(c.width * 0.705 + c.width * i * 0.0175),
            c.height * 0.05,
            c.point_radius * 2,
            c.point_radius * 2,
        )
        for i in range(colors_amount)
    ]


def create_text_mode_widget(surface: Surface) -> TextBox:
    """
    Returns a label - TextBox widget from pygame-widget,
    for color buttons.
    :param surface: Surface
    :return: TextBox
    """
    return TextBox(
        surface,
        x=ceil(c.width * 0.7),
        y=ceil(c.height * 0.053),
        width=0,
        height=0,
        fontSize=ceil(c.width * 0.015),
        textColour=c.text_color,
    )
