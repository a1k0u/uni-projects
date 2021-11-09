from random import randint
from math import sqrt, ceil
from collections import Counter
import pygame_widgets
import pygame
import pygame.gfxdraw
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
import colors

pygame.init()


def get_pos():
    return pygame.mouse.get_pos()


def change_color(color: list, func, number: int):
    return tuple(el + number if func(el) else el for el in color)


def calculate_distance(start: tuple, end: tuple):
    return sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)


class Application:
    def __init__(self, fps: int):
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.fps = fps

        self.application = True
        self.points = []
        self.nearest_points = []
        self.classify_points = []
        self.clock = pygame.time.Clock()
        self.radius = ceil(self.width * 0.005)
        self.menu_rect = pygame.Rect(0, 0, self.width, ceil(self.height * 0.1))
        self.classify_reset_flag = True
        self.user_color_index = 0

        self.mouse = (0, 0)
        self.parameters = {"points": self.width // 10, "colors": 3, "kNN": 3}
        self.colors = colors.POINT_COLORS[: self.parameters["colors"]]

        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.FULLSCREEN
        )

        self.generate_points()

        pygame.mouse.set_visible(False)

        sliders_type = {
            "points:": {
                "min": 2,
                "max": self.parameters["points"],
                "step": 20,
                "initial": self.parameters["points"] // 4,
            },
            "colors:": {
                "min": 2,
                "max": len(colors.POINT_COLORS),
                "step": 1,
                "initial": 2,
            },
            "kNN": {"min": 1, "max": 13, "step": 1, "initial": 3},
        }

        self.sliders_widget = [
            Slider(
                self.screen,
                x=ceil(self.width * 0.2 * i + self.width * 0.015),
                y=ceil(self.height * 0.053),
                width=self.width // 6,
                height=self.radius,
                min=sliders_type[key]["min"],
                max=sliders_type[key]["max"],
                step=sliders_type[key]["step"],
                initial=sliders_type[key]["initial"],
                colour=colors.SLIDER,
                handleRadius=self.radius,
                handleColour=colors.SLIDER_HANDLER,
            )
            for i, key in enumerate(sliders_type)
        ]

        self.text_widget = [
            TextBox(
                self.screen,
                x=ceil(self.width * 0.2 * i + self.width * 0.008),
                y=ceil(self.height * 0.053),
                width=0,
                height=0,
                fontSize=ceil(self.width * 0.015),
                textColour=colors.TEXT,
            )
            for i in range(len(sliders_type) + 1)
        ]

        self.toggle_widget = Toggle(
            self.screen,
            x=ceil(self.width * 0.617),
            y=ceil(self.height * 0.053),
            width=ceil(self.width * 0.02),
            height=ceil(self.width * 0.005),
            handleRadius=self.radius,
            startOn=True,
            onColour=colors.TEXT,
            offColour=colors.SLIDER,
            handleOnColour=colors.SLIDER_HANDLER,
            handleOffColour=colors.SLIDER_HANDLER,
        )

        self.text_edit_mode = TextBox(
            self.screen,
            x=ceil(self.width * 0.7),
            y=ceil(self.height * 0.053),
            width=0,
            height=0,
            fontSize=ceil(self.width * 0.015),
            textColour=colors.TEXT,
        )

        self.button_widget = []

    def loop(self):
        while self.application:
            self.mouse = get_pos()
            self.set_parameters()

            self.draw_background()
            if self.toggle_widget.getValue():
                if self.classify_reset_flag:
                    self.classify_area()
                    self.classify_reset_flag = False
                self.draw_classify_area()
            self.draw_points()
            self.draw_menu_bar()

            self.output_info()
            self.handlers()

            self.nearest_points = self.find_nearest(*self.mouse)
            if (
                not self.menu_rect.collidepoint(self.mouse)
                and not self.toggle_widget.getValue()
            ):
                self.draw_lines()
            self.draw_cursor()

            self.clock.tick(self.fps)
            pygame.display.update()

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.button_widget):
                    if button.collidepoint(self.mouse):
                        self.user_color_index = i
                if event.button == 1 and not self.menu_rect.collidepoint(self.mouse):
                    self.points.append(
                        [
                            self.mouse[0],
                            self.mouse[1],
                            self.colors[self.user_color_index]
                            if self.toggle_widget.getValue()
                            else self.find_common_color(self.find_nearest(*self.mouse)),
                        ]
                    )
                    self.classify_reset_flag = True
        pygame_widgets.update(events)

    def draw_gfx_circle(self, pos_x: int, pos_y: int, radius: int, color: tuple):
        pygame.gfxdraw.aacircle(self.screen, pos_x, pos_y, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, pos_x, pos_y, radius, color)

    def draw_points(self):
        for point in self.points:
            if self.toggle_widget.getValue():
                self.draw_gfx_circle(
                    point[0],
                    point[1],
                    self.radius + ceil(self.width * 0.0015),
                    colors.OUTLINE,
                )
                color = change_color(list(point[2]), lambda a: a, -92)
                self.draw_gfx_circle(point[0], point[1], self.radius, color)
                self.draw_gfx_circle(
                    point[0] - 1, point[1] - 1, self.radius - 1, point[2]
                )
            else:
                pygame.gfxdraw.circle(
                    self.screen, point[0], point[1], self.radius, point[2]
                )

    def draw_lines(self):
        for point in self.nearest_points:
            index = point[1]
            pos = (self.points[index][0], self.points[index][1])
            pygame.gfxdraw.line(
                self.screen,
                *self.mouse,
                *pos,
                colors.WHITE_ALPHA64,
            )
            self.draw_gfx_circle(*pos, ceil(self.radius * 0.3), colors.WHITE_ALPHA128)

    def draw_cursor(self):
        self.draw_gfx_circle(*self.mouse, ceil(self.radius * 0.75), colors.BLACK)
        self.draw_gfx_circle(*self.mouse, ceil(self.radius * 0.5), colors.WHITE)

    def draw_background(self):
        self.screen.fill(colors.BLACK)

    def draw_menu_bar(self):
        pygame.gfxdraw.box(self.screen, self.menu_rect, colors.BLACK)
        if self.toggle_widget.getValue():
            self.draw_color_buttons()

    def draw_classify_area(self):
        for rect in self.classify_points:
            pygame.gfxdraw.box(
                self.screen,
                [
                    rect[0],
                    rect[1],
                    self.radius + ceil(self.width * 0.0075),
                    self.radius + ceil(self.width * 0.0075),
                ],
                rect[2],
            )

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
                    radius + ceil(self.width * 0.001),
                    colors.WHITE,
                )
                self.draw_gfx_circle(
                    pos_x,
                    pos_y,
                    radius,
                    change_color(self.colors[i], lambda a: a, -64),
                )

    def generate_points(self):
        self.points = [
            [
                randint(self.radius, self.width - self.radius),
                randint(self.menu_rect.height, self.height - self.radius),
                self.colors[randint(0, len(self.colors) - 1)],
            ]
            for i in range(self.parameters["points"])
        ]

    def find_nearest(self, pos_x: int, pos_y: int):
        find_points = [
            [calculate_distance(point, (pos_x, pos_y)), i]
            for i, point in enumerate(self.points)
        ]
        find_points.sort(key=lambda a: a[0])

        return find_points[: min(self.parameters["kNN"], len(find_points))]

    def find_common_color(self, points: list):
        points_color = Counter([self.points[index[1]][2] for index in points])
        return points_color.most_common()[0][0]

    def classify_area(self):
        self.classify_points = [
            [
                x,
                y,
                change_color(
                    self.find_common_color(self.find_nearest(x, y)), lambda a: not a, 92
                ),
            ]
            for y in range(0, self.height, self.radius + ceil(self.width * 0.0088))
            for x in range(0, self.width, self.radius + ceil(self.width * 0.0088))
        ]

    def set_parameters(self):
        for i, key in enumerate(self.parameters):
            if self.parameters[key] != self.sliders_widget[i].getValue():
                self.classify_reset_flag = True
                self.parameters[key] = self.sliders_widget[i].getValue()
                self.colors = colors.POINT_COLORS[: self.parameters["colors"]]
                self.user_color_index = min(self.user_color_index, len(self.colors) - 1)
                self.generate_points()

                self.button_widget = [
                    pygame.Rect(
                        ceil(self.width * 0.705 + self.width * i * 0.0175),
                        self.height * 0.05,
                        self.radius * 2,
                        self.radius * 2,
                    )
                    for i in range(len(self.colors))
                ]

    def output_info(self):
        for i, key in enumerate(self.parameters):
            self.text_widget[i].setText(f"Amount of {key}: {self.parameters[key]}")
        self.text_widget[-1].setText(
            "Classify mode" if self.toggle_widget.getValue() else "Spider mode"
        )
        self.text_edit_mode.setText(
            "Choose color:" if self.toggle_widget.getValue() else ""
        )


if __name__ == "__main__":
    app = Application(fps=600)
    app.loop()
    pygame.quit()
