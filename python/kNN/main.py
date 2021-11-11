from random import randint
from collections import Counter

import pygame
import pygame.gfxdraw
import pygame_widgets

import widgets
import config as c
from app_math import change_color, calculate_distance, get_pos


class Application:
    def __init__(self):
        self.application = True
        self.classify_reset_flag = True

        self.points = []
        self.classify_blocks = []

        self.menu_rect = pygame.Rect(0, 0, c.width, c.menu_height)

        self.user_color_index = 0
        self.mouse = (0, 0)

        self.parameters = c.parameters
        self.colors = c.point_colors[: self.parameters["colors"]]

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((c.width, c.height), pygame.FULLSCREEN)
        pygame.display.set_caption(c.CAPTION)
        pygame.mouse.set_visible(False)

        self.generate_points()

        self.sliders_widget = widgets.create_slider_widgets(self.screen)
        self.text_widget = widgets.create_text_widgets(self.screen)
        self.toggle_widget = widgets.create_toggle_widget(self.screen)
        self.text_mode = widgets.create_text_mode_widget(self.screen)
        self.button_widget = widgets.create_color_buttons(len(self.colors))

    def loop(self):
        while self.application:
            self.update()
            self.draw()
            self.handlers()
            self.draw_cursor()

            self.clock.tick(c.FPS)
            pygame.display.update()

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_rect.collidepoint(self.mouse):
                    for i, button in enumerate(self.button_widget):
                        if button.collidepoint(event.pos):
                            self.user_color_index = i
                else:
                    self.points.append(
                        [
                            *event.pos,
                            self.colors[self.user_color_index]
                            if self.toggle_widget.getValue()
                            else self.find_common_color(self.find_nearest(*event.pos)),
                        ]
                    )
                    self.classify_reset_flag = True
        pygame_widgets.update(events)

    def update(self):
        self.mouse = get_pos()
        self.set_parameters()

    def set_parameters(self):
        for i, key in enumerate(self.parameters):
            if self.parameters[key] != self.sliders_widget[i].getValue():
                self.parameters[key] = self.sliders_widget[i].getValue()

                self.colors = c.point_colors[: self.parameters["colors"]]
                self.user_color_index = min(self.user_color_index, len(self.colors) - 1)

                self.classify_reset_flag = True
                self.button_widget = widgets.create_color_buttons(len(self.colors))

                self.generate_points()

    def draw(self):
        self.draw_background()

        if self.toggle_widget.getValue():
            if self.classify_reset_flag:
                self.classify_area()
                self.classify_reset_flag = False
            self.draw_classify_area()
        elif not self.menu_rect.collidepoint(self.mouse):
            self.draw_lines()

        self.draw_points()
        self.draw_menu_bar()

        self.output_info()

    def draw_background(self):
        self.screen.fill(c.black)

    def draw_classify_area(self):
        for pos_x, pos_y, color in self.classify_blocks:
            pygame.gfxdraw.box(
                self.screen,
                [
                    pos_x,
                    pos_y,
                    c.width_block,
                    c.width_block,
                ],
                color,
            )

    def draw_lines(self):
        nearest_points = self.find_nearest(*self.mouse)
        for index in nearest_points:
            pos = (self.points[index][0], self.points[index][1])
            pygame.gfxdraw.line(
                self.screen,
                *self.mouse,
                *pos,
                c.white_alpha_64,
            )
            self.draw_gfx_circle(*pos, c.line_radius, c.white_alpha_128)

    def draw_gfx_circle(self, pos_x: int, pos_y: int, radius: int, color: tuple):
        pygame.gfxdraw.aacircle(self.screen, pos_x, pos_y, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, pos_x, pos_y, radius, color)

    def draw_points(self):
        for pos_x, pos_y, color in self.points:
            if self.toggle_widget.getValue():
                changed_color = change_color(color, lambda a: a, c.MAKE_DARKER)

                self.draw_gfx_circle(
                    pos_x, pos_y, c.point_outline_radius, c.outline_color
                )
                self.draw_gfx_circle(pos_x, pos_y, c.point_radius, changed_color)
                self.draw_gfx_circle(pos_x - 1, pos_y - 1, c.point_radius - 1, color)
            else:
                pygame.gfxdraw.circle(self.screen, pos_x, pos_y, c.point_radius, color)

    def draw_menu_bar(self):
        pygame.gfxdraw.box(self.screen, self.menu_rect, c.black)
        if self.toggle_widget.getValue():
            self.draw_color_buttons()

    def draw_color_buttons(self):
        for i, button in enumerate(self.button_widget):
            pos_x, pos_y, *width = button
            radius = width[0] // 2
            pos_x += radius
            pos_y += radius

            self.draw_gfx_circle(pos_x, pos_y, radius, self.colors[i])
            if i == self.user_color_index:
                self.draw_gfx_circle(
                    pos_x,
                    pos_y,
                    radius + c.pressed_button_radius,
                    c.white,
                )
                self.draw_gfx_circle(
                    pos_x,
                    pos_y,
                    radius,
                    change_color(self.colors[i], lambda a: a, c.MAKE_DARKER_64),
                )

    def draw_cursor(self):
        self.draw_gfx_circle(*self.mouse, c.cursor_outline_radius, c.black)
        self.draw_gfx_circle(*self.mouse, c.cursor_radius, c.white)

    def generate_points(self):
        self.points = [
            [
                randint(c.point_radius, c.width - c.point_radius),
                randint(self.menu_rect.height, c.height - c.point_radius),
                self.colors[randint(0, len(self.colors) - 1)],
            ]
            for _ in range(self.parameters["points"])
        ]

    def find_nearest(self, pos_x: int, pos_y: int):
        find_points = [
            [calculate_distance(point, (pos_x, pos_y)), i]
            for i, point in enumerate(self.points)
        ]
        find_points.sort(key=lambda a: a[0])

        return [
            el[1] for el in find_points[: min(self.parameters["kNN"], len(find_points))]
        ]

    def find_common_color(self, points: list):
        points_color = Counter([self.points[index][2] for index in points])
        return points_color.most_common()[0][0]

    def classify_area(self):
        self.classify_blocks = [
            [
                x,
                y,
                change_color(
                    self.find_common_color(self.find_nearest(x, y)),
                    lambda a: not a,
                    c.MAKE_LIGHTER,
                ),
            ]
            for y in range(0, c.height, c.block_step)
            for x in range(0, c.width, c.block_step)
        ]

    def output_info(self):
        for i, key in enumerate(self.parameters):
            self.text_widget[i].setText(
                f"{c.SLIDERS_TEXT} {key}: {self.parameters[key]}"
            )
        self.text_widget[-1].setText(
            c.EDIT_MODE_TEXT if self.toggle_widget.getValue() else c.SPIDER_MODE_TEXT
        )
        self.text_mode.setText(
            c.BUTTONS_TEXT if self.toggle_widget.getValue() else c.NON_BUTTONS_TEXT
        )


if __name__ == "__main__":
    app = Application()
    app.loop()
    pygame.quit()
