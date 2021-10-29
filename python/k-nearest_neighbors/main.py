import pygame
from random import randint
import pygame.gfxdraw
from math import sqrt

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


def find_nearest(points: list, mouse: tuple) -> list:
	array = []
	for j in range(len(points)):
		cd = points[j][0]
		distance = sqrt((mouse[0] - cd[0])**2 + (mouse[1] - cd[1])**2)
		array.append((distance, j, points[j][1][0]))

	array = sorted(array, key=lambda x: x[0])[:5]
	return array[::]


def draw_line(points: list, nearest_p: list, mouse: tuple, screen):
	for i in range(len(nearest_p)):
		xy = points[nearest_p[i][1]][0]
		pygame.gfxdraw.line(screen, mouse[0], mouse[1], xy[0], xy[1], (255, 255, 255))
		pygame.gfxdraw.filled_circle(screen, mouse[0], mouse[1], 5, (255, 255, 255))
		pygame.gfxdraw.filled_circle(screen, xy[0], xy[1], 3, (255, 255, 255))


def main(width: int, height: int, fps: int):
	application = True
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((width, height), pygame.SHOWN)
	pygame.display.set_caption("")
	points = generate_points(width, height)
	pygame.mouse.set_visible(False)
	red, green = 0, 0
	while application:
		mouse = pygame.mouse.get_pos()
		p = find_nearest(points, mouse)
		for j in p:
			if j[2] == 0:
				green += 1
			else:
				red += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				application = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if red > green:
						points.append([mouse, (255, 0, 0)])
					elif green > red:
						points.append([mouse, (0, 255, 0)])

		red, green = 0, 0
		screen.fill((0, 0, 0))
		draw_points(points, 10, screen)
		draw_line(points, p, mouse, screen)
		pygame.display.update()
		clock.tick(fps)


if __name__ == "__main__":
	main(1920, 1080, 60)
	pygame.quit()
