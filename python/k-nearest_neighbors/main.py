import pygame
from random import randint
import pygame.gfxdraw

pygame.init()


def generate_points(width: int, height: int) -> list:
	points = []
	color = [(255, 0, 0), (0, 255, 0)]
	for i in range(0, width // 10):
		points.append([(randint(int(width * 0.05), width),
		                randint(int(height * 0.05), height)),
		               color[randint(0, len(color) - 1)]])
	return points


def draw_points(points: list, radius: int, screen):
	for point in points:
		pygame.gfxdraw.circle(screen, point[0][0], point[0][1], radius, point[1])


def find_nearest(points: list) -> list:
	array = []
	for j in points:
		pass


def main(width: int, height: int, fps: int):
	application = True
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((width, height), pygame.SHOWN)
	pygame.display.set_caption("")
	points = generate_points(width, height)
	while application:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				application = False

		screen.fill((0, 0, 0))
		draw_points(points, 10, screen)
		pygame.display.update()
		clock.tick(fps)


if __name__ == "__main__":
	main(800, 600, 60)
	pygame.quit()
