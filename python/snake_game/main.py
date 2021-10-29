import pygame

pygame.init()


def main(width: int, height: int, fps: int):
	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)
	application = True
	while application:
		pass


if __name__ == "__main__":
	main(1920, 1080, 5)
	pygame.quit()
