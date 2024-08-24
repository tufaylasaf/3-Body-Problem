import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60  # Frames per second

# Colors
BG = (30, 30, 30)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3 Body Problem")

# Clock to control the frame rate
clock = pygame.time.Clock()

g = 9.81 * 3  # Gravitational constant, reduced to avoid excessive acceleration
INITIAL_SPEED = 3  # Initial speed for the bodies


class Body:
    def __init__(self, mass, color, position, velocity):
        self.mass = mass
        self.color = color
        self.position = position
        self.velocity = velocity
        self.velocity.scale_to_length(INITIAL_SPEED)
        self.acceleration = pygame.Vector2(0, 0)
        self.trail = []
        self.max_trail_length = 5000

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.acceleration = pygame.Vector2(0, 0)

        # Add current position to trail
        self.trail.append(self.position.copy())

        # Limit trail length
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def attract(self, other):
        force = self.position - other.position
        distance = force.magnitude()

        # Avoid division by zero and apply a minimum distance
        if distance == 0:
            return

        force = force.normalize()  # Normalize to get direction
        strength = (g * self.mass * other.mass) / (distance**2)
        force = force * strength  # Scale by the calculated strength

        # Apply the force to both bodies
        self.apply_force(-force)  # This body is pulled towards 'other'
        other.apply_force(force)  # The other body is pulled towards this one

    def draw(self, screen):
        # Draw the trail
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail, self.mass // 3)

        pygame.draw.circle(screen, self.color, self.position, self.mass)

    def reset(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.velocity.scale_to_length(INITIAL_SPEED)
        self.acceleration = pygame.Vector2(0, 0)
        self.trail = []


# Function to create bodies
def create_bodies():
    a = Body(
        12,
        (255, 0, 0),
        pygame.Vector2(WIDTH // 7 * 3, HEIGHT // 2),
        pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
    )

    b = Body(
        12,
        (0, 0, 255),
        pygame.Vector2((WIDTH // 7) * 5, HEIGHT // 2),
        pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
    )

    c = Body(
        12,
        (0, 255, 0),
        pygame.Vector2((WIDTH // 2), HEIGHT // 3),
        pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
    )

    return [a, b]


# Initialize bodies
bodies = create_bodies()
dt = 1


# Main game loop
def main():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # If 'R' key is pressed
                    # Reset bodies
                    bodies[:] = create_bodies()

        # Calculate mutual attraction between bodies
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                bodies[i].attract(bodies[j])

        # Update game state
        for body in bodies:
            body.update(dt)

        # Fill the screen with BG color
        screen.fill(BG)

        # Draw everything
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
