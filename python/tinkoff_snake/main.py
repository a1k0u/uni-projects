from random import randrange
import pygame

pygame.init()


def random_pos():
    return randrange(SIZE, WIDTH - SIZE, SIZE), randrange(SIZE, WIDTH - SIZE, SIZE)


FPS = 5
WIDTH = 600
SIZE = 50

snake_x, snake_y = random_pos()
snake = [(snake_x, snake_y)]
snake_length = len(snake)

apple_pos = random_pos()

dx, dy = 0, -1


pygame.display.set_caption("Tinkoff's snake")
screen = pygame.display.set_mode((800, 600), pygame.SHOWN)
clock = pygame.time.Clock()


game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dx, dy = 0, -1
            if event.key == pygame.K_d:
                dx, dy = 1, 0
            if event.key == pygame.K_s:
                dx, dy = 0, 1
            if event.key == pygame.K_a:
                dx, dy = -1, 0

    snake_x += dx * SIZE
    snake_y += dy * SIZE

    snake.append((snake_x, snake_y))
    snake = snake[-snake_length:]

    if snake[-1] == apple_pos:
        snake_length += 1
        apple_pos = random_pos()

    screen.fill(pygame.Color("black"))
    for pos_x, pos_y in snake:
        pygame.draw.rect(screen, pygame.Color("yellow"), (pos_x, pos_y, SIZE-2, SIZE-2))
    pygame.draw.rect(screen, pygame.Color("red"), (*apple_pos, SIZE, SIZE))

    clock.tick(5)
    pygame.display.update()

pygame.quit()
