from math import sqrt
from random import randint
from collections import Counter
from pygame import mouse
import config as c


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


def find_nearest(points: list, value_knn: int, pos_x: int, pos_y: int) -> list:
    """
    Returns sorted list[distance, index] of
    value_knn nearest points.
    :param points: list
    :param value_knn: int
    :param pos_x: int
    :param pos_y: int
    :return: list
    """
    find_points = [
        [calculate_distance(point, (pos_x, pos_y)), i] for i, point in enumerate(points)
    ]
    find_points.sort(key=lambda a: a[0])

    return [el[1] for el in find_points[: min(value_knn, len(find_points))]]


def find_common_color(points: list, nearest_points: list) -> tuple:
    """
    Returns the most common color(tuple)
    among nearest points.
    :param points: list
    :param nearest_points: list
    :return: tuple
    """
    points_color = Counter([points[index][2] for index in nearest_points])
    return points_color.most_common()[0][0]


def generate_points(menu_height: int, colors: list, points_amount: int) -> list:
    """
    Returns list[x, y, color] of random generated points.
    :param menu_height: int
    :param colors: list
    :param points_amount: int
    :return: list
    """
    return [
        [
            randint(c.point_radius, c.width - c.point_radius),
            randint(menu_height, c.height - c.point_radius),
            colors[randint(0, len(colors) - 1)],
        ]
        for _ in range(points_amount)
    ]


def classify_area(points: list, value_knn: int) -> list:
    """
    Returns classified area list[x, y, color] of blocks.
    :param points: list
    :param value_knn: int
    :return: list
    """
    return [
        [
            x,
            y,
            change_color(
                find_common_color(points, find_nearest(points, value_knn, x, y)),
                lambda a: not a,
                c.MAKE_LIGHTER,
            ),
        ]
        for y in range(0, c.height, c.block_step)
        for x in range(0, c.width, c.block_step)
    ]
