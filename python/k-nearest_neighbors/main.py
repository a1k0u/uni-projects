from random import randint
from math import sqrt, ceil
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
    return tuple([el + number if func(el) else el for el in color])


class Application:
    def __init__(self, fps: int):
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.fps = fps

        self.application = True
        self.points = []
        self.nearest_points = []
        self.clock = pygame.time.Clock()
        self.radius = ceil(self.width * 0.005)
        self.height_menu = ceil(self.height * 0.1)
        self.classify_reset_flag = True

        self.mouse = (0, 0)
        self.parameters = {"points": self.width // 10, "colors": 2, "kNN": 3}
        self.colors = colors.POINT_COLORS[: self.parameters["colors"]]

        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.FULLSCREEN
        )

        self.generate_points()

        self.classify_points = []

        pygame.mouse.set_visible(False)

        sliders_type = {
            "points:": {
                "min": 1,
                "max": self.parameters["points"],
                "step": 10,
                "initial": self.parameters["points"] // 2,
            },
            "colors:": {
                "min": 2,
                "max": len(colors.POINT_COLORS),
                "step": 1,
                "initial": 2,
            },
            "kNN": {"min": 3, "max": 13, "step": 2, "initial": 3},
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

    def loop(self):
        while self.application:
            self.mouse = get_pos()
            self.set_parameters()
            if self.classify_reset_flag and self.toggle_widget.getValue():
                self.classify_area()
                self.classify_reset_flag = False

            self.draw_background()
            if self.toggle_widget.getValue():
                self.draw_classify_area()
            self.draw_points()
            self.draw_menu_bar()
            self.output_info()
            self.handlers()

            self.nearest_points = self.find_nearest(*self.mouse)
            if self.mouse[1] > self.height_menu and not self.toggle_widget.getValue():
                self.draw_lines()
            self.draw_cursor()

            pygame.display.update()
            self.clock.tick(self.fps)

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    event.button == 1
                    and self.mouse[1] > self.height_menu
                    and not self.toggle_widget.getValue()
                ):
                    self.points.append(
                        [
                            self.mouse[0],
                            self.mouse[1],
                            self.find_common_color(self.nearest_points),
                        ]
                    )
                    self.classify_reset_flag = True
        pygame_widgets.update(events)

    def draw_gfx_circle(self, x: int, y: int, radius: int, color: tuple):
        pygame.gfxdraw.aacircle(self.screen, x, y, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, x, y, radius, color)

    def draw_points(self):
        for point in self.points:
            if self.toggle_widget.getValue():
                self.draw_gfx_circle(
                    point[0], point[1], self.radius + 3, colors.OUTLINE
                )
                color = point[2]
                color = change_color(list(color), lambda a: a, -92)
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
        pygame.gfxdraw.box(
            self.screen, [0, 0, self.width, self.height_menu], colors.BLACK
        )

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

    def generate_points(self):
        self.points = [
            [
                randint(self.radius, self.width - self.radius),
                randint(self.height_menu, self.height - self.radius),
                self.colors[randint(0, len(self.colors) - 1)],
            ]
            for i in range(self.parameters["points"])
        ]

    def find_nearest(self, x, y):
        find_points = []
        for i, point in enumerate(self.points):
            distance = sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            find_points.append((distance, i))

        find_points.sort(key=lambda a: a[0])
        return find_points[: min(self.parameters["kNN"], len(find_points))]

    def find_common_color(self, points):
        points_color = {}
        for point in points:
            index = point[1]
            color = self.points[index][2]
            points_color.setdefault(color, 0)
            points_color[color] += 1
        return max(points_color, key=points_color.get)

    def classify_area(self):
        self.classify_points.clear()
        for y in range(0, self.height, self.radius + ceil(self.width * 0.0088)):
            for x in range(0, self.width, self.radius + ceil(self.width * 0.0088)):
                points = self.find_nearest(x, y)
                color = self.find_common_color(points)
                color = change_color(list(color), lambda a: not a, 92)
                self.classify_points.append([x, y, color])

    def set_parameters(self):
        if any(
            self.parameters[key] != self.sliders_widget[i].getValue()
            for i, key in enumerate(self.parameters)
        ):
            for i, key in enumerate(self.parameters):
                self.parameters[key] = self.sliders_widget[i].getValue()
            self.colors = colors.POINT_COLORS[: self.parameters["colors"]]
            self.generate_points()
            self.classify_area()

    def output_info(self):
        for i, key in enumerate(self.parameters):
            self.text_widget[i].setText(f"Amount of {key}: {self.parameters[key]}")
        self.text_widget[-1].setText(
            "Classify mode" if self.toggle_widget.getValue() else "Edit mode"
        )


if __name__ == "__main__":
    app = Application(fps=600)
    app.loop()
    pygame.quit()
