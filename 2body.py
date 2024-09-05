import random
import pygame
import sys
from body import Body


pygame.init()


WIDTH, HEIGHT = 550, 550
FPS = 60


BG = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3 Body Problem")


clock = pygame.time.Clock()


def create_bodies():
    a = Body(
        1,
        13,
        (84, 13, 110),
        pygame.Vector2(-0.5, 0),
        pygame.Vector2(0, 0.5),
    )

    b = Body(
        1,
        13,
        (214, 40, 40),
        pygame.Vector2(0.5, 0),
        pygame.Vector2(0, -0.5),
    )

    return [a, b]


bodies = create_bodies()
dt = 0.01


def main():
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for body in bodies:
            body.verlet_update(dt, bodies)

        screen.fill(BG)

        for body in bodies:
            body.draw_trail(screen)

        for body in bodies:
            body.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
