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
        self.mouse = (0, 0)
        self.parameters = c.parameters

        self.space = pymunk.Space()
        self.space.gravity = 0, self.parameters["gravity"]
        self.options = pymunk.pygame_util.DrawOptions(self.screen)

        self.create_wall = False
        self.create_wall_st_pos = (0, 0)

        self.initialization_static_obj()

        self.sliders_widget = wdg.create_slider_widgets(self.screen)
        self.texts_widget = wdg.create_text_widgets(self.screen)
        self.menu = pygame.Rect(*c.menu_bar_draw)
        self.rect = pygame.Rect(*c.menu_bar_rect)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.application = False

                if event.key == pygame.K_BACKSPACE:
                    for o in self.space.shapes:
                        self.space.remove(o)
                    self.objects.clear()
                    self.initialization_static_obj()

            if not self.rect.collidepoint(self.mouse):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        obj.create_dynamic_balls(
                            self.space, event.pos, self.parameters, self.objects
                        )
                    elif event.button == 3:
                        if not self.create_wall:
                            self.create_wall = True
                            self.create_wall_st_pos = event.pos

                if event.type == pygame.MOUSEBUTTONUP:
                    if (
                        self.create_wall_st_pos != event.pos
                        and self.create_wall
                        and event.button == 3
                    ):
                        obj.create_wall(
                            self.space,
                            self.create_wall_st_pos,
                            event.pos,
                            c.walls_width,
                            c.walls_color,
                            self.objects,
                        )
                    self.create_wall = False
                    self.create_wall_st_pos = (0, 0)
        pygame_widgets.update(events)

    def update(self):
        self.mouse = get_pos()
        for i, key in enumerate(self.parameters):
            self.parameters[key] = self.sliders_widget[i].getValue()

        for o, body, shape in self.objects:
            if o == "wall":
                shape.elasticity = self.parameters["wall_elasticity"]
            else:
                shape.elasticity = self.parameters["ball_elasticity"]
            shape.friction = self.parameters["friction"]
        self.space.gravity = (0, self.parameters["gravity"])

        self.update_text()

    def update_text(self):
        for i, text in enumerate(c.text_widget):
            msg = text
            if i < len(self.sliders_widget):
                msg += f": {self.sliders_widget[i].getValue()}"
            self.texts_widget[i].setText(msg)

    def draw(self):
        self.draw_background()
        self.space.debug_draw(self.options)
        self.preview_creating_walls()
        self.draw_menu_bar()

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

    def draw_menu_bar(self):
        pygame.draw.rect(self.screen, c.background_color, self.menu)

    def initialization_static_obj(self):
        pos_y, step = c.pins_height, c.pins_step
        for column in range(c.pins_column):
            pos_x = -1.5 * step if column % 2 else -step
            for _ in range(c.pins_row):
                obj.create_static_balls(
                    self.space, (pos_x, pos_y), c.pins_color, self.objects
                )
                if column == c.pins_column - 1:
                    obj.create_wall(
                        self.space,
                        (pos_x, pos_y + step),
                        (pos_x, c.height),
                        c.walls_width // 2,
                        c.funnel_wall_color,
                        self.objects,
                    )
                pos_x += step
            pos_y += 0.5 * step

        for walls in [
            c.walls_coord.values(),
            c.funnel_coord_left.values(),
            c.funnel_coord_right.values(),
        ]:
            for pos_st, pos_end, width in walls:
                obj.create_wall(
                    self.space, pos_st, pos_end, width, c.walls_color, self.objects
                )


if __name__ == "__main__":
    app = Application()
    app.loop()

    pygame.quit()
