import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 600
REDUCED_WIDTH, REDUCED_HEIGHT = 256, 256

class VisualEngine:
    def __init__(self, screen):
        self.screen = screen
        self.zoom = random.uniform(0.8, 1.2)
        self.pan_x = random.uniform(-0.5, 0.5)
        self.pan_y = random.uniform(-0.5, 0.5)

    def draw_fractal(self):
        """Draw the fractal on the screen using numpy for faster computation."""
        fractal_surface = pygame.Surface((REDUCED_WIDTH, REDUCED_HEIGHT))
        x = np.linspace(-2, 2, REDUCED_WIDTH) / (0.5 * self.zoom) + self.pan_x
        y = np.linspace(-2, 2, REDUCED_HEIGHT) / (0.5 * self.zoom) + self.pan_y
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        c = Z
        img_array = np.zeros((REDUCED_WIDTH, REDUCED_HEIGHT, 3), dtype=np.uint8)
        for i in range(32):  # Reduced iterations for performance
            Z = Z * Z + c
            mask = np.abs(Z) < 1000
            img_array[mask, 0] = (i % 8 * 32) + img_array[mask, 0]
            img_array[mask, 1] = (i % 16 * 16) + img_array[mask, 1]
            img_array[mask, 2] = (i % 32 * 8) + img_array[mask, 2]
        pygame.surfarray.blit_array(fractal_surface, img_array)
        upscaled_fractal = pygame.transform.scale(fractal_surface, (WIDTH, HEIGHT))
        self.screen.blit(upscaled_fractal, (0, 0))
        return np.mean(img_array)  # Return average brightness

    def update(self, brightness):
        """Update the fractal's parameters for animation."""
        # Smooth panning
        self.pan_x += random.uniform(-0.002, 0.002)
        self.pan_y += random.uniform(-0.002, 0.002)

        # Dynamic zoom influenced by brightness
        base_zoom_factor = 1.02  # Base zoom speed
        modulation = (brightness / 255) * 0.03  # Modulation based on brightness
        self.zoom *= base_zoom_factor + modulation
