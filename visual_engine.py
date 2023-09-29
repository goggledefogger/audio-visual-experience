import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600

class VisualEngine:
    def __init__(self, screen):
        self.screen = screen
        self.zoom = 1
        self.pan_x = 0
        self.pan_y = 0

    def draw_fractal(self):
        """Draw the fractal on the screen."""
        for x in range(WIDTH):
            for y in range(HEIGHT):
                zx, zy = x / (0.5 * self.zoom * WIDTH) + self.pan_x, y / (0.5 * self.zoom * HEIGHT) + self.pan_y
                c = zx + zy * 1j
                z = c
                for i in range(128):  # Reduced iterations for faster rendering
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                r, g, b = i % 8 * 32, i % 16 * 16, i % 32 * 8
                self.screen.set_at((x, y), (r, g, b))

    def update(self):
        """Update the fractal's parameters for animation."""
        self.zoom *= 1.02
        self.pan_x += 0.002
        self.pan_y += 0.001
