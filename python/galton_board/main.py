import pygame
import config as c


class Application:
    def __init__(self):
        self.application = True

        self.screen = pygame.display.set_mode((c.width, c.height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

    def loop(self):
        while self.application:
            self.handlers()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(c.fps)

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False

    def update(self):
        pass

    def draw(self):
        self.draw_background()

    def draw_background(self):
        self.screen.fill(c.background_color)


if __name__ == "__main__":
    app = Application()
    app.loop()

    pygame.quit()
