from random import randrange
import pymunk.pygame_util
import config as c


def create_balls(
    space: pymunk.Space,
    pos: tuple,
    parameters: dict,
    objects: list
) -> None:
    """
    Function is creating some amount of dynamic balls with
    exact parameters and adding this objects into
    pymunk space.
    :param space: pymunk.Space
    :param pos: tuple
    :param parameters: dict
    :param objects: list
    :return: None
    """
    for _ in range(c.cparameters["amount"]):
        ball_moment = pymunk.moment_for_circle(
            c.cparameters["mass"], 0, c.cparameters["radius"]
        )

        ball_body = pymunk.Body(c.cparameters["mass"], ball_moment)
        ball_body.position = (pos[0] + randrange(20), pos[1] + randrange(10))

        ball_shape = pymunk.Circle(ball_body, c.cparameters["radius"])
        ball_shape.elasticity = parameters["elasticity"]
        ball_shape.friction = parameters["friction"]
        ball_shape.color = [randrange(255) for _ in range(4)]

        space.add(ball_body, ball_shape)
        objects.append(("ball", ball_body, ball_shape))


def create_wall(space: pymunk.Space, pos_start: tuple, pos_end: tuple, objects: list) -> None:
    """
    Function is creating a static segment shape(wall)
    and adding this object into pymunk space.
    :param space: pymunk.Space
    :param pos_start: tuple
    :param pos_end: tuple
    :param objects: list
    :return: None
    """
    segment_shape = pymunk.Segment(space.static_body, pos_start, pos_end, c.walls_width)
    segment_shape.elasticity = c.parameters["walls_elasticity"]
    segment_shape.color = c.walls_color

    space.add(segment_shape)
    objects.append(("wall", segment_shape, segment_shape))
