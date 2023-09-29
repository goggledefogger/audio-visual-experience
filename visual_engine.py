import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
REDUCED_WIDTH, REDUCED_HEIGHT = WIDTH // 2, HEIGHT // 2  # Half the resolution

class VisualEngine:
    def __init__(self, screen):
        self.screen = screen
        self.zoom = 1
        self.pan_x = 0
        self.pan_y = 0

    def draw_fractal(self):
        """Draw the fractal on the screen."""
        fractal_surface = pygame.Surface((REDUCED_WIDTH, REDUCED_HEIGHT))
        for x in range(REDUCED_WIDTH):
            for y in range(REDUCED_HEIGHT):
                zx, zy = x / (0.5 * self.zoom * REDUCED_WIDTH) + self.pan_x, y / (0.5 * self.zoom * REDUCED_HEIGHT) + self.pan_y
                c = zx + zy * 1j
                z = c
                for i in range(128):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                r, g, b = i % 8 * 32, i % 16 * 16, i % 32 * 8
                fractal_surface.set_at((x, y), (r, g, b))

        # Upscale the reduced resolution fractal to fit the screen
        upscaled_fractal = pygame.transform.scale(fractal_surface, (WIDTH, HEIGHT))
        self.screen.blit(upscaled_fractal, (0, 0))

    def update(self):
        """Update the fractal's parameters for animation."""
        self.zoom *= 1.02
        self.pan_x += 0.002
        self.pan_y += 0.001
