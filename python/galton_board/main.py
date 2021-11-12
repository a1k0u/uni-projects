import pygame
import pymunk.pygame_util

import config as c
import objects as obj


def get_pos():
    return pygame.mouse.get_pos()


class Application:
    def __init__(self):
        self.application = True
        pymunk.pygame_util.positive_y_is_up = False

        self.screen = pygame.display.set_mode((c.width, c.height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.space.gravity = c.gravity
        self.options = pymunk.pygame_util.DrawOptions(self.screen)

        self.ball_parameters = c.ball_parameters

        self.create_wall = False
        self.create_wall_pos = (0, 0)

        self.mouse = (0, 0)

        for value in c.walls_coord.values():
            obj.create_wall(self.space, value[0], value[1])

    def loop(self):
        while self.application:
            self.handlers()
            self.update()
            self.draw()

            pygame.display.update()
            self.space.step(1 / c.FPS)
            self.clock.tick(c.FPS)

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    obj.create_balls(self.space, event.pos, self.ball_parameters)
                elif event.button == 3:
                    if not self.create_wall:
                        self.create_wall = True
                        self.create_wall_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if self.create_wall_pos != (0, 0):
                    obj.create_wall(self.space, self.create_wall_pos, event.pos)

                    self.create_wall = False
                    self.create_wall_pos = (0, 0)

    def update(self):
        self.mouse = get_pos()

    def draw(self):
        self.draw_background()

        self.space.debug_draw(self.options)
        self.preview_creating_walls()

    def draw_background(self):
        self.screen.fill(c.background_color)

    def preview_creating_walls(self):
        if self.create_wall:
            pygame.draw.line(
                self.screen,
                c.walls_color,
                self.create_wall_pos,
                self.mouse,
                width=c.walls_width,
            )


if __name__ == "__main__":
    app = Application()
    app.loop()

    pygame.quit()
