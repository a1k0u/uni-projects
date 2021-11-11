import pygame
import pymunk.pygame_util

import config as c
import objects as obj


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

        obj.create_walls(self.space)

    def loop(self):
        while self.application:
            self.handlers()
            self.update()
            self.draw()

            pygame.display.update()
            self.space.step(1 / c.fps)
            self.clock.tick(c.fps)

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                obj.create_balls(self.space, event.pos, self.ball_parameters)

    def update(self):
        pass

    def draw(self):
        self.draw_background()

        self.space.debug_draw(self.options)

    def draw_background(self):
        self.screen.fill(c.background_color)


if __name__ == "__main__":
    app = Application()
    app.loop()

    pygame.quit()
