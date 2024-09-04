import random
import pygame
import sys
from body import Body

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60  # Frames per second

# Colors
BG = (0, 0, 0)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3 Body Problem")

# Clock to control the frame rate
clock = pygame.time.Clock()


# Function to create bodies
def create_bodies():
    a = Body(
        1,
        12,
        (255, 0, 0),
        pygame.Vector2(-1, 0),
        pygame.Vector2(0.347113, 0.532727),
    )

    b = Body(
        1,
        12,
        (0, 0, 255),
        pygame.Vector2(0, 0),
        pygame.Vector2(-0.694226, -1.065454),
    )

    c = Body(
        1,
        12,
        (0, 255, 0),
        pygame.Vector2(1, 0),
        pygame.Vector2(0.347113, 0.532727),
    )

    return [a, b, c]


# Initialize bodies
bodies = create_bodies()
dt = 0.01


# Main game loop
def main():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for body in bodies:
            # body.simulate(bodies)
            body.update(dt, bodies)

        # Fill the screen with BG color
        screen.fill(BG)

        # # Draw everything
        for body in bodies:
            body.draw_trail(screen)

        for body in bodies:
            body.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
