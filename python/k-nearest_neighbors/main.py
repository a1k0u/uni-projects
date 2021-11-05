from random import randint
from math import sqrt, ceil
import pygame_widgets
import pygame
import pygame.gfxdraw
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import colors

pygame.init()


def get_pos():
    return pygame.mouse.get_pos()


class Application:
    def __init__(self, fps: int):
        display_info = pygame.display.Info()
        self.width = 1024
        self.height = 768
        self.fps = fps

        self.application = True
        self.points = []
        self.find_points = []
        self.clock = pygame.time.Clock()
        self.radius = ceil(self.width * 0.005)

        self.mouse = (0, 0)
        self.parameters = {"points": self.width // 10, "colors": 2, "kNN": 3}
        self.colors = colors.POINT_COLORS[: self.parameters["colors"]]

        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.FULLSCREEN
        )

        self.generate_points()

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
            "kNN": {"min": 3, "max": 21, "step": 2, "initial": 3},
        }

        self.sliders_widget = [
            Slider(
                self.screen,
                x=ceil(self.width * 0.2 * i + self.width * 0.015),
                y=ceil(self.height * 0.035),
                width=self.width // 6,
                height=self.radius,
                min=sliders_type[key]["min"],
                max=sliders_type[key]["max"],
                step=sliders_type[key]["step"],
                initial=sliders_type[key]["initial"],
                colour=(128, 128, 128),
                handleRadius=self.radius,
                handleColour=colors.ORANGE,
            )
            for i, key in enumerate(sliders_type)
        ]

        self.text_widget = [
            TextBox(
                self.screen,
                x=ceil(self.width * 0.2 * i + self.width * 0.01),
                y=ceil(self.height * 0.030),
                width=0,
                height=0,
                fontSize=ceil(self.width * 0.015),
                textColour=colors.WHITE,
            )
            for i in range(len(sliders_type))
        ]

    def loop(self):
        while self.application:
            self.mouse = get_pos()
            self.set_parameters()
            self.draw_background()
            self.find_nearest()
            self.handlers()
            self.draw_points()
            if self.mouse[1] > self.height * 0.1:
                self.draw_lines()
            self.draw_cursor()
            self.output_info()
            pygame.display.update()
            self.clock.tick(self.fps)

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points_color = {}
                    for point in self.find_points:
                        index = point[1]
                        color = self.points[index][1]
                        points_color.setdefault(color, 0)
                        points_color[color] += 1
                    self.points.append(
                        [self.mouse, max(points_color, key=points_color.get)]
                    )
        pygame_widgets.update(events)

    def set_parameters(self):
        if any(
            self.parameters[key] != self.sliders_widget[i].getValue()
            for i, key in enumerate(self.parameters)
        ):
            for i, key in enumerate(self.parameters):
                self.parameters[key] = self.sliders_widget[i].getValue()
            self.colors = colors.POINT_COLORS[: self.parameters["colors"]]
            self.generate_points()

    def output_info(self):
        for i, key in enumerate(self.parameters):
            self.text_widget[i].setText(f"Amount of {key}: {self.parameters[key]}")

    def draw_points(self):
        for point in self.points:
            pygame.gfxdraw.circle(
                self.screen, point[0][0], point[0][1], self.radius, point[1]
            )

    def draw_lines(self):
        for point in self.find_points:
            index = point[1]
            pos = self.points[index][0]
            pygame.gfxdraw.line(
                self.screen,
                self.mouse[0],
                self.mouse[1],
                pos[0],
                pos[1],
                colors.WHITE_ALPHA64,
            )
            pygame.gfxdraw.filled_circle(
                self.screen,
                pos[0],
                pos[1],
                ceil(self.radius * 0.2),
                colors.WHITE_ALPHA128,
            )

    def draw_cursor(self):
        pygame.gfxdraw.filled_circle(
            self.screen,
            self.mouse[0],
            self.mouse[1],
            ceil(self.radius * 0.5),
            colors.WHITE,
        )

    def draw_background(self):
        self.screen.fill(colors.BLACK)

    def generate_points(self):
        self.points = [
            [
                (
                    randint(self.radius, self.width - self.radius),
                    randint(ceil(self.height * 0.1), self.height - self.radius),
                ),
                self.colors[randint(0, len(self.colors) - 1)],
            ]
            for i in range(self.parameters["points"])
        ]

    def find_nearest(self):
        self.find_points.clear()
        for i, point in enumerate(self.points):
            distance = sqrt(
                (self.mouse[0] - point[0][0]) ** 2 + (self.mouse[1] - point[0][1]) ** 2
            )
            self.find_points.append((distance, i))

        self.find_points.sort(key=lambda x: x[0])
        self.find_points = self.find_points[
            : min(self.parameters["kNN"], len(self.find_points))
        ]


if __name__ == "__main__":
    app = Application(fps=600)
    app.loop()
    pygame.quit()
