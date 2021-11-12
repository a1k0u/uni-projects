import pygame
import pymunk.pygame_util
import pygame_widgets

import config as c
import objects as obj
import widgets as wdg


def get_pos():
    return pygame.mouse.get_pos()


class Application:
    def __init__(self):
        self.application = True
        pymunk.pygame_util.positive_y_is_up = False

        self.screen = pygame.display.set_mode((c.width, c.height), c.screen_mode)
        self.clock = pygame.time.Clock()

        self.objects = []
        self.parameters = c.parameters

        self.space = pymunk.Space()
        self.space.gravity = self.parameters["gravity"]
        self.options = pymunk.pygame_util.DrawOptions(self.screen)

        self.create_wall = False
        self.create_wall_st_pos = (0, 0)
        self.mouse = (0, 0)

        for value in c.walls_coord.values():
            obj.create_wall(self.space, value[0], value[1], self.objects)

        self.sliders = wdg.create_slider_widgets(self.screen)

    def loop(self):
        while self.application:
            self.draw()
            self.handlers()
            self.update()

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
                    obj.create_balls(self.space, event.pos, self.parameters, self.objects)
                elif event.button == 3:
                    if not self.create_wall:
                        self.create_wall = True
                        self.create_wall_st_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.create_wall_st_pos != event.pos and self.create_wall and event.button == 3:
                    obj.create_wall(self.space, self.create_wall_st_pos, event.pos, self.objects)
                self.create_wall = False
                self.create_wall_st_pos = (0, 0)
        pygame_widgets.update(events)

    def update(self):
        self.mouse = get_pos()
        for i, key in enumerate(self.parameters):
            self.parameters[key] = self.sliders[i].getValue()

        for o, body, shape in self.objects:
            if o == "wall":
                shape.elasticity = self.parameters["walls_elasticity"]
            else:
                shape.elasticity = self.parameters["elasticity"]
            shape.friction = self.parameters["friction"]
        self.space.gravity = (0, self.parameters["gravity"])

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
                self.create_wall_st_pos,
                self.mouse,
                width=c.walls_width,
            )


if __name__ == "__main__":
    app = Application()
    app.loop()

    pygame.quit()
