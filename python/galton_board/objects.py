from random import randrange
import pymunk.pygame_util
import config as c


def create_balls(
    space: pymunk.Space,
    pos: tuple,
    parameters: dict,
) -> None:
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


def create_walls(space: pymunk.Space) -> None:
    walls_coord = {
        "left": [(0, 0), (0, c.height)],
        "right": [(c.width, 0), (c.width, c.height)],
        "bottom": [(0, c.height), (c.width, c.height)],
    }

    for pos in walls_coord.values():
        segment_shape = pymunk.Segment(space.static_body, pos[0], pos[1], c.walls_width)
        segment_shape.elasticity = c.walls_elasticity
        space.add(segment_shape)
