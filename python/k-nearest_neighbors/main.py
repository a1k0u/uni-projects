import pygame
import pygame.gfxdraw
import colors
from random import randint
from math import sqrt, ceil

pygame.init()


def get_pos():
    return pygame.mouse.get_pos()


class Application:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps

        self.application = True
        self.points = []
        self.find_points = []
        self.clock = pygame.time.Clock()
        self.lines = 7
        self.mouse = (0, 0)
        self.points_types = 6
        self.radius = ceil(self.width * 0.005)
        self.colors = colors.POINT_COLORS[: self.points_types]
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.generate_points()

        pygame.display.set_caption("")
        pygame.mouse.set_visible(False)

    def loop(self):
        while self.application:
            self.mouse = get_pos()
            self.find_nearest()
            self.handlers()
            self.draw_background()
            self.draw_points()
            self.draw_lines()
            self.draw_cursor()

            pygame.display.update()
            self.clock.tick(self.fps)

    def handlers(self):
        for event in pygame.event.get():
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

    def draw_points(self):
        for point in self.points:
            pygame.gfxdraw.circle(
                self.screen, point[0][0], point[0][1], self.radius, point[1]
            )

    def draw_lines(self):
        for point in self.find_points:
            index = point[1]
            cd = self.points[index][0]
            pygame.gfxdraw.line(
                self.screen,
                self.mouse[0],
                self.mouse[1],
                cd[0],
                cd[1],
                colors.WHITE_ALPHA64,
            )
            pygame.gfxdraw.filled_circle(
                self.screen, cd[0], cd[1], ceil(self.radius * 0.2), colors.WHITE_ALPHA128
            )

    def draw_cursor(self):
        pygame.gfxdraw.filled_circle(
            self.screen, self.mouse[0], self.mouse[1], ceil(self.radius * 0.5), colors.WHITE
        )

    def draw_background(self):
        self.screen.fill(colors.BLACK)

    def generate_points(self):
        self.points = [
            [
                (
                    randint(self.radius, self.width - self.radius),
                    randint(self.radius, self.height - self.radius),
                ),
                self.colors[randint(0, len(self.colors) - 1)],
            ]
            for i in range(self.width // 10)
        ]

    def find_nearest(self):
        self.find_points.clear()
        for i, point in enumerate(self.points):
            distance = sqrt(
                (self.mouse[0] - point[0][0]) ** 2 + (self.mouse[1] - point[0][1]) ** 2
            )
            self.find_points.append((distance, i))

        self.find_points.sort(key=lambda x: x[0])
        self.find_points = self.find_points[: min(self.lines, len(self.find_points))]


if __name__ == "__main__":
    app = Application(width=1920, height=1080, fps=60)
    app.loop()
    pygame.quit()
