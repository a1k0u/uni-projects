from random import randrange
import pymunk.pygame_util
import config as c


def create_balls(
    space: pymunk.Space,
    pos: tuple,
    parameters: dict,
) -> None:
    """
    Function is creating some amount of dynamic balls with
    exact parameters and adding this objects into
    pymunk space.
    :param space: pymunk.Space
    :param pos: tuple
    :param parameters: dict
    :return: None
    """
    for _ in range(parameters["amount"]):
        ball_moment = pymunk.moment_for_circle(
            parameters["mass"], 0, parameters["radius"]
        )

        ball_body = pymunk.Body(parameters["mass"], ball_moment)
        ball_body.position = (pos[0] + randrange(10), pos[1] + randrange(10))

        ball_shape = pymunk.Circle(ball_body, parameters["radius"])
        ball_shape.elasticity = parameters["elasticity"]
        ball_shape.friction = parameters["friction"]
        ball_shape.color = [randrange(255) for _ in range(4)]

        space.add(ball_body, ball_shape)


def create_wall(space: pymunk.Space, pos_start: tuple, pos_end: tuple) -> None:
    """
    Function is creating a static segment shape(wall)
    and adding this object into pymunk space.
    :param space: pymunk.Space
    :param pos_start: tuple
    :param pos_end: tuple
    :return: None
    """
    segment_shape = pymunk.Segment(space.static_body, pos_start, pos_end, c.walls_width)
    segment_shape.elasticity = c.walls_elasticity
    segment_shape.color = c.walls_color
    space.add(segment_shape)
