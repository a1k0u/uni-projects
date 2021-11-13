from random import randrange
import pymunk.pygame_util
import config as c


def add_parameters(
    space: pymunk.Space,
    body,
    shape,
    obj_type: str,
    elasticity: float,
    friction: float,
    color: tuple,
    objects: list,
) -> None:
    """
    Function is adding some parameters: elasticity,
    friction, color, for pymunk objects and connect
    these shapes to the pymunk space.
    :param space: pymunk.Space
    :param body:
    :param shape:
    :param obj_type: str
    :param elasticity: float
    :param friction: float
    :param color: tuple
    :param objects: list
    :return: None
    """
    shape.elasticity = elasticity
    shape.friction = friction
    shape.color = color

    if body is shape:
        space.add(shape)
    else:
        space.add(body, shape)
    objects.append((obj_type, body, shape))


def create_dynamic_balls(
    space: pymunk.Space, pos: tuple, parameters: dict, objects: list
) -> None:
    """
    Function is creating some amount of dynamic
    balls with exact parameters.
    :param space: pymunk.Space
    :param pos: tuple
    :param parameters: dict
    :param objects: list
    :return: None
    """
    for _ in range(parameters["ball_amount"]):
        ball_moment = pymunk.moment_for_circle(
            parameters["ball_mass"], 0, parameters["ball_radius"]
        )

        ball_body = pymunk.Body(parameters["ball_mass"], ball_moment)
        ball_body.position = (pos[0] + randrange(20), pos[1] + randrange(20))

        ball_shape = pymunk.Circle(ball_body, parameters["ball_radius"])
        add_parameters(
            space,
            ball_body,
            ball_shape,
            "ball",
            parameters["ball_elasticity"],
            parameters["friction"],
            [randrange(255) for _ in range(4)],
            objects,
        )


def create_static_balls(
    space: pymunk.Space, pos: tuple, color: tuple, objects: list
) -> None:
    """
    Function is creating a static ball with
    exact position, radius, color.
    :param space: pymunk.Space
    :param pos: tuple
    :param color: tuple
    :param objects: list
    :return: None
    """
    ball_shape = pymunk.Circle(space.static_body, c.pins_radius, offset=pos)
    print(c.parameters)
    add_parameters(
        space,
        ball_shape,
        ball_shape,
        "ball",
        c.parameters["wall_elasticity"],
        c.parameters["friction"],
        color,
        objects,
    )


def create_wall(
    space: pymunk.Space,
    pos_start: tuple,
    pos_end: tuple,
    width: int,
    color: tuple,
    objects: list,
) -> None:
    """
    Function is creating a static
    segment shape(wall).
    :param space: pymunk.Space
    :param pos_start: tuple
    :param pos_end: tuple
    :param width: int
    :param color: tuple
    :param objects: list
    :return: None
    """
    segment_shape = pymunk.Segment(space.static_body, pos_start, pos_end, width)
    add_parameters(
        space,
        segment_shape,
        segment_shape,
        "wall",
        c.parameters["wall_elasticity"],
        c.parameters["friction"],
        color,
        objects,
    )
