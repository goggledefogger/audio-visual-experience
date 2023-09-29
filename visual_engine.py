import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 600

class VisualEngine:
    def __init__(self, screen):
        self.screen = screen
        self.points = [(WIDTH/2, HEIGHT/2)]
        self.vertices = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(3)]
        self.zoom = 1
        self.pan_x = 0
        self.pan_y = 0
        self.color_palette = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) for _ in range(3)]
        for _ in range(10000):  # Pre-generate the fractal points
            chosen_vertex = random.choice(self.vertices)
            last_point = self.points[-1]
            new_point = ((last_point[0] + chosen_vertex[0]) / 2, (last_point[1] + chosen_vertex[1]) / 2)
            self.points.append(new_point)

    def draw_fractal(self):
        """Draw the fractal on the screen."""
        for point in self.points:
            color = random.choice(self.color_palette)
            pygame.draw.circle(self.screen, color, (int(point[0]), int(point[1])), 1)

    def update(self):
        """Update the fractal's parameters for animation."""
        self.zoom *= random.uniform(1.01, 1.03)
        self.pan_x += random.uniform(-1, 1)
        self.pan_y += random.uniform(-1, 1)
        self.points = [(p[0] * self.zoom + self.pan_x, p[1] * self.zoom + self.pan_y) for p in self.points]

        # Reset zoom and pan if the fractal goes off-screen
        if self.zoom > 2.5:
            self.zoom = 1
            self.pan_x = 0
            self.pan_y = 0
            self.points = [(WIDTH/2, HEIGHT/2)]
