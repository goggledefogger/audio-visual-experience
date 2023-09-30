import pygame
import numpy as np
import random
import math
import colorsys

# Constants
WIDTH, HEIGHT = 800, 600
REDUCED_WIDTH, REDUCED_HEIGHT = 256, 256

class Noise:
    def __init__(self):
        self.x = 0  # We only need 1D noise for this

    def generate(self):
        self.x += 0.01  # Adjust this to control frequency of noise changes
        # This generates a smoothly changing series of numbers between -1 and 1
        return (2 * (0.5 - float((math.sin((self.x + math.sin(self.x)) * math.pi) % 1))))

class VisualEngine:
    def __init__(self, screen):
        self.screen = screen
        self.zoom = random.uniform(0.8, 1.2)
        self.pan_x = random.uniform(-0.5, 0.5)
        self.pan_y = random.uniform(-0.5, 0.5)
        self.zoom_noise = Noise()
        self.target_pan_x = self.pan_x
        self.target_pan_y = self.pan_y
        self.pan_speed = 0.002
        self.color_shift = 0
        self.target_color_shift = 0
        self.frame_count = 0


    def lerp(self, start, end, t):
        """Linear interpolation function. Returns a value between start and end."""
        return start * (1 - t) + end * t

    def draw_fractal(self):
        """Draw the fractal on the screen using numpy for faster computation."""
        fractal_surface = pygame.Surface((REDUCED_WIDTH, REDUCED_HEIGHT))
        x = np.linspace(-2, 2, REDUCED_WIDTH) / (0.5 * self.zoom) + self.pan_x
        y = np.linspace(-2, 2, REDUCED_HEIGHT) / (0.5 * self.zoom) + self.pan_y
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        c = Z
        img_array = np.zeros((REDUCED_WIDTH, REDUCED_HEIGHT, 3), dtype=np.uint8)
        # Compute color_shift from frame_count to slow down color change rate
        color_shift = self.frame_count / 500.0  # Slow down color change rate; adjust the denominator for finer control
        for i in range(32):
            Z = Z * Z + c
            mask = np.abs(Z) < 1000
            # Compute color_shift from frame_count to slow down color change rate
            color_shift_period = 500.0  # Adjust the denominator for finer control
            # cycle between 0 and 1
            color_shift = (self.frame_count / color_shift_period) % 1
            # Convert from HSV to RGB
            r, g, b = colorsys.hsv_to_rgb(color_shift, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)  # Convert to integers
            img_array[mask, 0] += np.clip((img_array[mask, 0] + r) // 2, 0, 255)
            img_array[mask, 1] += np.clip((img_array[mask, 1] + g) // 2, 0, 255)
            img_array[mask, 2] += np.clip((img_array[mask, 2] + b) // 2, 0, 255)
        pygame.surfarray.blit_array(fractal_surface, img_array)
        upscaled_fractal = pygame.transform.scale(fractal_surface, (WIDTH, HEIGHT))
        self.screen.blit(upscaled_fractal, (0, 0))
        return np.mean(img_array)  # Return average brightness

    def update(self, brightness):
        # Increment frame_count
        self.frame_count += 1
        """Update the fractal's parameters for animation."""
        # Smooth panning
        self.pan_x += random.uniform(-0.002, 0.002)
        self.pan_y += random.uniform(-0.002, 0.002)

        # Dynamic zoom influenced by brightness
        base_zoom_factor = 1.02  # Base zoom speed
        modulation = (brightness / 255) * 0.03  # Modulation based on brightness
        zoom_noise = self.zoom_noise.generate()  # Generate noise
        self.zoom *= base_zoom_factor + modulation + (zoom_noise * 0.01)  # Apply noise to zoom
        # Note: we multiply noise by 0.01 to tone down impact
        # Compute color_shift from frame_count to slow down color change rate
        self.color_shift = (self.color_shift + 1) % 1  # Keep the hue between 0 and 1

        # If there is a considerable shift and we have crossed 100 frames, update target color shift
        if abs(self.color_shift - self.target_color_shift) < 0.01 or self.frame_count % 100 == 0:
            self.target_color_shift = self.frame_count / 500.0  # or set target to random value with random.random()
            self.target_color_shift %= 1

        # Smoothly transition color shift

        self.color_shift = self.lerp(self.color_shift, self.target_color_shift, 0.01)  # 0.01 sets the speed of transition

        # Adjust pan scale based on zoom for smoother motion at high zoom levels
        pan_scale = self.pan_speed / self.zoom

        # Adjust pan target towards areas of high contrast
        frame = pygame.surfarray.array3d(self.screen)
        standard_deviation = np.std(frame)
        self.target_pan_x += standard_deviation * random.uniform(-pan_scale, pan_scale)
        self.target_pan_y += standard_deviation * random.uniform(-pan_scale, pan_scale)

        # Update the pan values using linear interpolation for smoother transitions
        self.pan_x = self.lerp(self.pan_x, self.target_pan_x, 0.01)
        self.pan_y = self.lerp(self.pan_y, self.target_pan_y, 0.01)
