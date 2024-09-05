import pygame
import pygame.gfxdraw
import numpy as np


class Body:
    def __init__(self, mass, radius, color, position, velocity):
        self.mass = mass
        self.radius = radius
        self.color = color
        self.position = position
        self.velocity = velocity
        self.acceleration = pygame.Vector2(0, 0)
        self.trail = []
        self.max_trail_length = 5000
        self.scaledPos = pygame.Vector2(0, 0)
        self.initial = np.array([position, velocity])

    def update(self, dt, bodies):

        self.initial = self.initial + self.rk4(self.initial, dt, bodies)
        pos, vel = self.initial
        self.position = pygame.Vector2(pos[0], pos[1])

        # Add the current position to the trail
        scale = 200
        x = self.position.x * scale + 275
        y = self.position.y * scale + 275
        self.scaledPos = pygame.Vector2(x, y)
        self.trail.append(self.scaledPos)

        # Ensure the trail length doesn't exceed the maximum limit
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def verlet_update(self, dt, bodies):
        # Compute the initial acceleration based on the current forces
        initial_acc = self.compute_acceleration(bodies)
        
        # Update the position using Velocity Verlet
        self.position += self.velocity * dt + 0.5 * initial_acc * dt**2

        # Compute the new acceleration after updating the position
        new_acc = self.compute_acceleration(bodies)
        
        # Update the velocity using the average of the current and new acceleration
        self.velocity += 0.5 * (initial_acc + new_acc) * dt

        # Add the current position to the trail (scaled)
        scale = 200
        x = self.position.x * scale + 275
        y = self.position.y * scale + 275
        self.scaledPos = pygame.Vector2(x, y)
        self.trail.append(self.scaledPos)

        # Ensure the trail length doesn't exceed the maximum limit
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def compute_acceleration(self, bodies):
        acc = pygame.Vector2(0, 0)
        for body in bodies:
            if body == self:
                continue
            r = body.position - self.position
            distance = r.magnitude()
            acc += body.mass * r / distance**3
        return acc

    def draw(self, screen):
        x = int(self.scaledPos.x)
        y = int(self.scaledPos.y)
        pygame.gfxdraw.aacircle(screen, x, y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, x, y, self.radius, self.color)

    def draw_trail(self, screen):
        if len(self.trail) > 1:
            pygame.draw.aalines(screen, self.color, False, self.trail, 1)

    def motion(self, y, bodies):
        pos, vel = y
        acc = pygame.Vector2(0, 0)
        for body in bodies:
            if body == self:
                continue
            r = body.position - pos
            distance = r.magnitude()
            acc += body.mass * r / distance**3

        return np.array([vel, acc])

    def rk4(self, y, dt, bodies):
        k1 = self.motion(y, bodies)
        k2 = self.motion(y + 0.5 * k1 * dt, bodies)
        k3 = self.motion(y + 0.5 * k2 * dt, bodies)
        k4 = self.motion(y + k3 * dt, bodies)

        return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
