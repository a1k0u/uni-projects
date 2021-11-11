import pygame
import pymunk.pygame_util
import config as c


class Application:
    def __init__(self):
        self.application = True
        pymunk.pygame_util.positive_y_is_up = False

        self.screen = pygame.display.set_mode((c.width, c.height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.space.gravity = 0, 1000

        self.options = pymunk.pygame_util.DrawOptions(self.screen)

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
