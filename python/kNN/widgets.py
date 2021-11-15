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
            x=ceil(c.slider_pos_x_step * i + c.slider_pos_x),
            y=ceil(c.slider_pos_y),
            width=c.slider_width,
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
        x=ceil(c.toggle_pos_x),
        y=ceil(c.toggle_pos_y),
        width=ceil(c.toggle_width),
        height=ceil(c.toggle_height),
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
            x=ceil(c.text_pos_x_step * i + c.text_pos_x),
            y=ceil(c.text_pos_y),
            width=0,
            height=0,
            fontSize=ceil(c.text_font_size),
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
            ceil(c.button_color_pos_x + c.button_color_pos_x_step * i),
            ceil(c.button_color_pos_y),
            c.button_color_size,
            c.button_color_size,
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
        x=ceil(c.text_mode_pos_x),
        y=ceil(c.text_mode_pos_y),
        width=0,
        height=0,
        fontSize=ceil(c.text_font_size),
        textColour=c.text_color,
    )
