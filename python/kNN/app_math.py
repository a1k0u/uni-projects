from math import sqrt
from pygame import mouse


def get_pos() -> tuple:
    """
    Returns coordinates of user's computer mouse.
    :return: tuple
    """
    return mouse.get_pos()


def change_color(color: list, func, number: int) -> tuple:
    """
    Returns tuple with three components: r, g, b channels.
    Their tone has been changed by some number and some
    lambda function, which increment or decrement value
    for following channels.
    :param color: list
    :param func: lambda
    :param number: number
    :return: tuple
    """
    return tuple(el + number if func(el) else el for el in color)


def calculate_distance(start: tuple, end: tuple) -> float:
    """
    Returns float number value of distance between
    two points on the surface by Pythagoras formula.
    :param start: int
    :param end: int
    :return: float
    """
    return sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
