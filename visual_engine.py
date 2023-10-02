import pygame
import numpy as np
import random
import colorsys
import math
import noise
import time

# Constants
WIDTH, HEIGHT = 800, 600
REDUCED_WIDTH, REDUCED_HEIGHT = 256, 256

class VisualEngine:
    def valmorphanize(self):
        """Default Valmorphanize effect. Can be overridden by subclasses."""
        pass

    # Class for a Basic Fractal
    class MandleBrot:
        def __init__(self, screen):
            self.screen = screen
            self.zoom = random.uniform(0.8, 1.2)
            self.pan_x = random.uniform(-0.5, 0.5)
            self.pan_y = random.uniform(-0.5, 0.5)

        def draw(self):
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

        def update(self, brightness=100):
            """Update the fractal's parameters for animation."""
            # Smooth panning
            self.pan_x += random.uniform(-0.002, 0.002)
            self.pan_y += random.uniform(-0.002, 0.002)

            # Dynamic zoom influenced by brightness
            base_zoom_factor = 1.02  # Base zoom speed
            modulation = (brightness / 255) * 0.03  # Modulation based on brightness
            self.zoom *= base_zoom_factor + modulation

        def valmorphanize(self):
            # Change zoom, pan values with large differences
            self.zoom = random.uniform(0.5, 2)
            self.pan_x = random.uniform(-1, 1)
            self.pan_y = random.uniform(-1, 1)


    # Class for another type of Fractal

    class Triforce:
        def __init__(self, screen):
            self.screen = screen
            self.reset_fractal()

        def reset_fractal(self):
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.vertices = [(WIDTH // 2, 50), (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)]
            self.current_point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.points_drawn = 0
            self.directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(3)]
            self.bg_color = (random.randint(10, 50), random.randint(10, 50), random.randint(10, 50))

        def draw(self):
            # Draw a subtle gradient background
            gradient_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            gradient_surface.fill((*self.bg_color, 5))
            self.screen.blit(gradient_surface, (0, 0))

            # Draw the moving vertices with trails
            for vertex, direction in zip(self.vertices, self.directions):
                pygame.draw.circle(self.screen, (255, 255, 255, 50), vertex, 5)

            for _ in range(1000):  # Draw 1000 points per frame for smoother animation
                chosen_vertex = random.choice(self.vertices)
                new_x = (self.current_point[0] + chosen_vertex[0]) // 2
                new_y = (self.current_point[1] + chosen_vertex[1]) // 2
                self.current_point = (new_x, new_y)
                gradient_color = (
                    (self.color[0] + new_x) % 255,
                    (self.color[1] + new_y) % 255,
                    (self.color[2] + new_x + new_y) % 255
                )
                point_size = 1 + (new_x + new_y) % 3  # Vary point size between 1 and 3
                pygame.draw.circle(self.screen, (*gradient_color, 150), self.current_point, point_size)
                self.points_drawn += 1

        def update(self):
            # Move the vertices in a controlled manner
            for i in range(3):
                if 0 < self.vertices[i][0] < WIDTH:
                    self.vertices[i] = (self.vertices[i][0] + self.directions[i][0], self.vertices[i][1])
                else:
                    self.directions[i] = (-self.directions[i][0], self.directions[i][1])
                if 0 < self.vertices[i][1] < HEIGHT:
                    self.vertices[i] = (self.vertices[i][0], self.vertices[i][1] + self.directions[i][1])
                else:
                    self.directions[i] = (self.directions[i][0], -self.directions[i][1])
            # Gradually change the base color
            self.color = ((self.color[0] + 1) % 255, (self.color[1] + 2) % 255, (self.color[2] + 3) % 255)
            # Gradually change the background color
            self.bg_color = ((self.bg_color[0] + 1) % 60, (self.bg_color[1] + 1) % 60, (self.bg_color[2] + 1) % 60)

        def valmorphanize(self):
            # Reset to fully randomize
            self.reset_fractal()

    class MultiSpirograph:
        def __init__(self, screen):
            self.screen = screen
            self.t = 0
            self.bg_hue = random.random()
            self.spirographs = [self._create_spirograph() for _ in range(3)]  # Create 3 spirographs

        def _create_spirograph(self):
            R = random.randint(50, 150)
            r = random.randint(25, 125)
            l = random.uniform(0.5, 1.0)
            hue = random.random()
            color = colorsys.hsv_to_rgb(hue, 0.8, 0.8)  # High saturation and value for vibrant colors
            color = tuple(int(c * 255) for c in color)
            return {"R": R, "r": r, "l": l, "color": color, "points": []}

        def draw(self):
            bg_color = colorsys.hsv_to_rgb(self.bg_hue, 0.3, 0.3)  # Low saturation and value for subdued background
            bg_color = tuple(int(c * 255) for c in bg_color)
            self.screen.fill(bg_color)
            for spiro in self.spirographs:
                for point in spiro["points"]:
                    pygame.draw.circle(self.screen, spiro["color"], (int(point[0]), int(point[1])), 1)

        def update(self):
            for spiro in self.spirographs:
                x = (spiro["R"] + spiro["r"]) * np.cos(self.t) - spiro["l"] * spiro["r"] * np.cos((spiro["R"] + spiro["r"]) * self.t / spiro["r"])
                y = (spiro["R"] + spiro["r"]) * np.sin(self.t) - spiro["l"] * spiro["r"] * np.sin((spiro["R"] + spiro["r"]) * self.t / spiro["r"])

                # Translate the points for visualization
                px = int(x + WIDTH / 2)
                py = int(y + HEIGHT / 2)

                spiro["points"].append((px, py))

                if len(spiro["points"]) > 5000:  # Keep the last 5000 points for performance
                    spiro["points"].pop(0)

            self.t += 0.05
            self.bg_hue = (self.bg_hue + 0.001) % 1.0  # Slowly change the background hue

        def valmorphanize(self):
            for spiro in self.spirographs:
                # Clear the points to reset the drawing
                spiro["points"].clear()

                # Randomize spirograph parameters
                spiro["R"] = random.randint(50, 150)
                spiro["r"] = random.randint(25, 125)
                spiro["l"] = random.uniform(0.5, 1.0)

                # Randomize color
                hue = random.random()
                color = colorsys.hsv_to_rgb(hue, 0.8, 0.8)  # High saturation and value for vibrant colors
                spiro["color"] = tuple(int(c * 255) for c in color)

            # Randomize background hue
            self.bg_hue = random.random()


    class DragonCurve:
        def __init__(self, screen):
            self.screen = screen
            self.iterations = 12  # Number of iterations
            self.axiom = "FX"  # Initial state
            self.rules = {
                "X": "X+YF+",
                "Y": "-FX-Y"
            }
            self.angle = 90  # 90 degrees
            self.length = 5
            self.commands = self._generate_commands()
            self.current_step = 0  # Current step in the animation
            self.color_gradient = [(255, i, 255 - i) for i in range(256)]
            self.speed_modulation_factor = 10000

        def _generate_commands(self):
            result = self.axiom
            for _ in range(self.iterations):
                next_result = ""
                for char in result:
                    next_result += self.rules.get(char, char)
                result = next_result
            return result

        def draw(self):
            self.screen.fill((0, 0, 0))
            x, y = WIDTH // 2, HEIGHT // 2
            direction = 0  # Starting direction is right

            for i, command in enumerate(self.commands):
                if i > self.current_step:
                    break
                color = self.color_gradient[i % 256]
                if command == "F":
                    new_x = x + self.length * np.cos(direction)
                    new_y = y + self.length * np.sin(direction)
                    pygame.draw.line(self.screen, color, (x, y), (new_x, new_y))
                    x, y = new_x, new_y
                elif command == "+":
                    direction += np.radians(self.angle)
                elif command == "-":
                    direction -= np.radians(self.angle)

        def update(self):
            # Create a seasonal speed modulation using multiple sine functions
            seasonal_speed = np.sin(self.speed_modulation_factor) * np.sin(self.speed_modulation_factor * 0.1)
            speed = 5 + 50 * seasonal_speed  # Oscillate between fast and average speeds

            self.current_step += int(speed)
            self.speed_modulation_factor += 0.05  # Adjust this for faster/slower oscillations

            if self.current_step > len(self.commands):
                self.current_step = 0  # Reset animation
                self.speed_modulation_factor = 0  # Reset modulation factor

        def valmorphanize(self):
            # invert angle
            self.angle *= -1
            # randomize the speed modulation factor
            self.speed_modulation_factor = random.uniform(7000, 15000)
            # randomize color gradient
            self.color_gradient = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(256)]
            # Change length of each segment
            self.length = random.randint(1, 10)
            # Reset the commands
            self.commands = self._generate_commands()
            # Reset current step
            self.current_step = 0

    class ColorfulSpirograph:
        def __init__(self, screen):
            self.screen = screen
            self.width, self.height = screen.get_size()
            self.max_circles = random.randint(3, 7)
            self.color_angles = [random.uniform(0, 360) for _ in range(self.max_circles)]
            self.initial_radii = [random.randint(20, min(self.width, self.height) // 6) for _ in range(self.max_circles)]
            self.radii = self.initial_radii.copy()
            self.speeds = [random.uniform(0.01, 0.04) for _ in range(self.max_circles)]
            self.bg_hue = random.randint(0, 360)
            self.time = 0
            self.pulse_frequency = random.uniform(1, 5)
            self.thickness_factor = 1
            self.start_x = self.width // 2
            self.start_y = self.height // 2
            self.bg_pulse = 0

        def draw_gradient_background(self):
            avg_hue = sum(self.color_angles) / len(self.color_angles)
            top_color = pygame.Color(0)
            bottom_color = pygame.Color(0)
            top_color.hsva = ((avg_hue + int(10 * np.sin(self.bg_pulse))) % 360, 50, 85, 100)
            bottom_color.hsva = ((avg_hue + 180 + int(10 * np.sin(self.bg_pulse))) % 360, 50, 65, 100)

            for y in range(self.height):
                blend = y / self.height
                color = top_color.lerp(bottom_color, blend)
                pygame.draw.line(self.screen, color, (0, y), (self.width, y))

        def draw(self):
            self.draw_gradient_background()

            for i in range(len(self.color_angles)):
                for _ in range(10):
                    x = self.start_x + self.radii[i] * np.cos(self.color_angles[i])
                    y = self.start_y + self.radii[i] * np.sin(self.color_angles[i])

                    color = pygame.Color(0)
                    hue_variation = int(30 * np.sin(self.time + i))
                    color.hsva = ((self.color_angles[i] + hue_variation) % 360, 60, 80, 100)

                    circle_size = int(3 * self.thickness_factor * (1 + np.sin(self.time)))
                    pygame.draw.circle(self.screen, color, (int(x), int(y)), circle_size)

                    self.color_angles[i] += self.speeds[i]
                    oscillation = self.initial_radii[i] * 0.2 * np.sin(self.time)  # Oscillation of 20% of initial radius
                    self.radii[i] = self.initial_radii[i] + oscillation

            self.bg_hue += 0.5
            self.time += 0.01

        def update(self):
            self.bg_pulse += 0.01

        def valmorphanize(self):
            self.thickness_factor = random.choice([1.5, 0.7, 1])
            self.thickness_factor = max(min(self.thickness_factor, 2), 0.5)
            self.pulse_frequency = random.uniform(1, 5)
            self.max_circles = random.randint(3, 7)

            while len(self.color_angles) < self.max_circles:
                self.color_angles.append(random.uniform(0, 360))
                new_radius = random.randint(20, min(self.width, self.height) // 6)
                self.radii.append(new_radius)
                self.initial_radii.append(new_radius)  # Update initial_radii
                self.speeds.append(random.uniform(0.01, 0.04))

            while len(self.color_angles) > self.max_circles:
                idx = random.randint(0, len(self.color_angles) - 1)
                self.color_angles.pop(idx)
                self.radii.pop(idx)
                self.initial_radii.pop(idx)  # Update initial_radii
                self.speeds.pop(idx)

            # Occasionally boost the radii to make the spirograph bigger
            if random.random() < 0.5:  # 50% chance to boost the radii
                boost_factor = random.uniform(1.1, 1.5)  # Boost by 10% to 50%
                self.radii = [int(r * boost_factor) for r in self.radii]

            # Ensure radii don't exceed screen dimensions
            self.radii = [min(r, min(self.width, self.height) // 4) for r in self.radii]

            self.start_x = random.randint(self.width // 4, 3 * self.width // 4)
            self.start_y = random.randint(self.height // 4, 3 * self.height // 4)

    class PointillismPattern:
        def __init__(self, screen):
            self.screen = screen
            self.dots = []
            self.max_dots = 500
            self.time = 0
            self.bg_color1 = pygame.Color(255, 255, 255)
            self.bg_color2 = pygame.Color(200, 200, 255)

        def draw(self):
            # Smooth background color transition
            blend = (np.sin(self.time) + 1) / 2  # Oscillates between 0 and 1
            color = self.bg_color1.lerp(self.bg_color2, blend)
            self.screen.fill(color)

            # Adjust max_dots dynamically
            self.max_dots = int(400 + 100 * np.sin(self.time))

            # Add new dots
            while len(self.dots) < self.max_dots:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.uniform(1, 3)
                growth_rate = random.uniform(0.1, 0.3)
                hue = (x + y + int(200 * np.sin(self.time))) % 360
                color = pygame.Color(0)
                color.hsva = (hue, 100, 100, random.randint(50, 100))
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
                wave_factor = random.uniform(0.1, 0.5)
                self.dots.append([x, y, size, growth_rate, color, dx, dy, wave_factor])

            # Draw and update dots
            for dot in self.dots:
                pygame.draw.circle(self.screen, dot[4], (dot[0], dot[1]), int(dot[2]))
                dot[2] += dot[3] * np.sin(self.time * dot[7])  # Pulsating size
                dot[0] += dot[5] + dot[7] * np.sin(self.time)
                dot[1] += dot[6] + dot[7] * np.cos(self.time)
                dot[4].hsva = ((dot[4].hsva[0] + 1) % 360, 100, 100, 100)  # Slight color shift

                if dot[2] > 20 or dot[2] < 1 or dot[0] < 0 or dot[0] > WIDTH or dot[1] < 0 or dot[1] > HEIGHT:
                    self.dots.remove(dot)

            self.time += 0.02

        def update(self):
            # Slowly change the background colors
            self.bg_color1.hsva = ((self.bg_color1.hsva[0] + 1) % 360, 100, 100, 100)
            self.bg_color2.hsva = ((self.bg_color2.hsva[0] - 1) % 360, 100, 100, 100)

        def valmorphanize(self):
            # Change maximum number of dots
            self.max_dots = random.randint(100, 1000)

            # Change background colors
            self.bg_color1 = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.bg_color2 = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    class HexagonTessellation:
        def __init__(self, screen):
            self.screen = screen
            self.time = 0
            self.angle = 0
            self.base_hue = random.random()  # Randomly choose a base hue
            self.palette = self.generate_palette()
            self.zoom_direction = 1  # 1 for zooming in, -1 for zooming out
            self.zoom_factor = 1
            self.pan_x = 0
            self.pan_y = 0
            self.pan_speed_x = random.choice([-1, 1]) * 0.5
            self.pan_speed_y = random.choice([-1, 1]) * 0.5
            self.bg_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(4)]
            self.valmorphanize_duration = 0
            self.original_speed_multiplier = 1

        def generate_palette(self):
            palette = []
            for i in range(8):
                hue = (self.base_hue + i/8) % 1  # Vary the hue around the base hue
                color = pygame.Color(0)
                color.hsla = (hue * 360, 100, 50, 100)  # Convert HSL to RGB
                palette.append(color)
            return palette

        def lerp_color(self, color1, color2, alpha):
            r = int(color1.r * (1 - alpha) + color2.r * alpha)
            g = int(color1.g * (1 - alpha) + color2.g * alpha)
            b = int(color1.b * (1 - alpha) + color2.b * alpha)
            return pygame.Color(r, g, b)

        def draw(self):
            gradient = pygame.Surface((WIDTH, HEIGHT))
            top_color = pygame.Color(50, 50, 50)
            bottom_color = pygame.Color(20, 20, 20)
            for y in range(HEIGHT):
                alpha = y / HEIGHT
                color = self.lerp_color(top_color, bottom_color, alpha)
                pygame.draw.line(gradient, color, (0, y), (WIDTH, y))
            self.screen.blit(gradient, (0, 0))

            base_hex_size = 45
            rows = int(HEIGHT // (1.5 * base_hex_size))
            cols = int(WIDTH // (np.sqrt(3) * base_hex_size))
            alpha = self.time % 1
            for row in range(rows + 1):
                for col in range(cols + 1):
                    hex_size = base_hex_size + 15 * np.sin(2 * self.time + row + col)
                    x = col * np.sqrt(3) * base_hex_size * self.zoom_factor + self.pan_x
                    y = row * 1.5 * base_hex_size * self.zoom_factor + self.pan_y
                    if col % 2 == 1:
                        y += 0.75 * base_hex_size * self.zoom_factor
                    color = self.lerp_color(self.palette[row % 8], self.palette[col % 8], alpha)
                    color_alpha = int(100 * (0.7 + 0.3 * np.sin(self.time)))  # Calculate opacity modulation
                    color.hsla = (color.hsla[0], color.hsla[1], color.hsla[2], color_alpha)  # Set the alpha value
                    self.draw_hexagon(x, y, color, hex_size)

        def draw_hexagon(self, x, y, color, hex_size):
            hexagon = []
            for i in range(6):
                angle = 2 * np.pi / 6 * (i + self.angle)
                xi = x + hex_size * np.cos(angle)
                yi = y + hex_size * np.sin(angle)
                hexagon.append((xi, yi))
            pygame.draw.polygon(self.screen, color, hexagon)
            pygame.draw.polygon(self.screen, (30, 30, 30), hexagon, 2)  # Border

        def update(self):
            self.angle += 0.01
            self.time += 0.005
            self.zoom_factor += 0.005 * self.zoom_direction
            if self.zoom_factor > 1.2 or self.zoom_factor < 0.8:
                self.zoom_direction *= -1
            self.pan_x += self.pan_speed_x
            self.pan_y += self.pan_speed_y
            if abs(self.pan_x) > WIDTH * 0.2:
                self.pan_speed_x *= -1
            if abs(self.pan_y) > HEIGHT * 0.2:
                self.pan_speed_y *= -1
            if self.valmorphanize_duration > 0:
                self.valmorphanize_duration -= 1
                if self.valmorphanize_duration == 0:
                    self.speed_multiplier = self.original_speed_multiplier
                    self.hex_size_multiplier = 1

        def valmorphanize(self):
            self.base_hue = random.random()
            self.palette = self.generate_palette()
            self.angle = 3.14 if random.random() > 0.5 else 0
            self.pan_speed_x *= random.choice([-1, 1])
            self.pan_speed_y *= random.choice([-1, 1])
            self.time = random.uniform(0, 10)
            self.zoom_factor = random.uniform(0.5, 1.5)

    class Starfield:
        def __init__(self, screen):
            self.screen = screen
            self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random()) for _ in range(200)]
            self.direction = 1  # 1 for outward, -1 for inward
            self.speed_boost = 1

        def draw(self):
            self.screen.fill((0, 0, 0))
            for x, y, z in self.stars:
                color = (int(255 * z), int(255 * z), 255)
                pygame.draw.circle(self.screen, color, (int(x), int(y)), int(5 * z))

        def update(self):
            new_stars = []
            for x, y, z in self.stars:
                x += self.direction * self.speed_boost * (x - WIDTH // 2) * z * 0.05
                y += self.direction * self.speed_boost * (y - HEIGHT // 2) * z * 0.05
                if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                    new_stars.append((x, y, z))
                else:
                    new_stars.append((random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random()))
            self.stars = new_stars
            if self.speed_boost > 1:
                self.speed_boost *= 0.98  # Gradually reduce the speed boost

        def valmorphanize(self):
            self.speed_boost = 5  # Increase speed for a short burst

    class WavePattern:
        def __init__(self, screen):
            self.screen = screen
            self.time = 0
            self.inverted = 1  # 1 for normal wave, -1 for inverted wave
            self.frequency_shift = 1
            self.color_shift = 0

        def draw(self):
            # Background gradient
            start_color = (50, 50, 150)
            end_color = (150, 50, 50)
            for i in range(HEIGHT):
                alpha = i / HEIGHT
                color = (
                    int((1 - alpha) * start_color[0] + alpha * end_color[0]),
                    int((1 - alpha) * start_color[1] + alpha * end_color[1]),
                    int((1 - alpha) * start_color[2] + alpha * end_color[2])
                )
                pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

            for x in range(0, WIDTH, 10):
                amplitude = 100 + 30 * math.sin(self.time / 2)
                y1 = int(HEIGHT / 2 + self.inverted * amplitude * math.sin(self.frequency_shift * x / 50 + self.time))
                y2 = int(HEIGHT / 2 + self.inverted * (amplitude - 20) * math.sin(self.frequency_shift * x / 30 + 2 * self.time + 1))
                y3 = int(HEIGHT / 2 + self.inverted * (amplitude - 40) * math.sin(self.frequency_shift * x / 20 + 3 * self.time + 2))

                color1 = (int(255 * (math.sin(self.color_shift) + 1) / 2), 255, 255)
                color2 = (255, int(255 * (math.sin(self.color_shift + 2) + 1) / 2), 255)
                color3 = (255, 255, int(255 * (math.sin(self.color_shift + 4) + 1) / 2))

                pygame.draw.circle(self.screen, color1, (x, y1), 5 + 2 * math.sin(x / 50 + self.time))
                pygame.draw.circle(self.screen, color2, (x, y2), 5 + 2 * math.sin(x / 30 + 2 * self.time))
                pygame.draw.circle(self.screen, color3, (x, y3), 5 + 2 * math.sin(x / 20 + 3 * self.time))

        def update(self):
            self.time += 0.1
            self.color_shift += 0.05

        def valmorphanize(self):
            self.frequency_shift = random.uniform(0.5, 1.5)  # Random frequency shift

    class RotatingSpiral:
        def __init__(self, screen):
            self.screen = screen
            self.angle = 0
            self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
            self.speed = 0.05
            self.arms = 200
            self.bird_positions = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
            self.bird_angles = [random.uniform(0, 2 * math.pi) for _ in range(10)]
            self.bird_speeds = [random.uniform(0.01, 0.03) for _ in range(10)]

        def draw_bird_silhouette(self, x, y, angle):
            # Transformations for rotation
            s, c = math.sin(angle), math.cos(angle)

            # Body of the bird
            pygame.draw.ellipse(self.screen, (200, 200, 200), (x, y, 60, 30))

            # Wing of the bird
            wing_points = [(x+30, y), (x+60, y-20), (x, y-20)]
            wing_points_rotated = [(x + c*(px-x) - s*(py-y), y + s*(px-x) + c*(py-y)) for px, py in wing_points]
            pygame.draw.polygon(self.screen, (200, 200, 200), wing_points_rotated)

            # Tail of the bird
            tail_points = [(x, y+15), (x-20, y+30), (x, y+30)]
            tail_points_rotated = [(x + c*(px-x) - s*(py-y), y + s*(px-x) + c*(py-y)) for px, py in tail_points]
            pygame.draw.polygon(self.screen, (200, 200, 200), tail_points_rotated)

        def draw(self):
            # Background effect with moving and rotating bird pattern
            for i, (x, y) in enumerate(self.bird_positions):
                self.draw_bird_silhouette(x, y, self.bird_angles[i])
                self.bird_positions[i] = (x + self.bird_speeds[i] * math.cos(self.bird_angles[i]),
                                        y + self.bird_speeds[i] * math.sin(self.bird_angles[i]))
                self.bird_angles[i] += 0.01  # Slowly rotate the birds

                # Wrap the birds around the screen
                if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
                    self.bird_positions[i] = (x % WIDTH, y % HEIGHT)

            for i in range(1, self.arms, 2):
                x_pos = int(WIDTH / 2 + i * math.cos(self.angle + i))
                y_pos = int(HEIGHT / 2 + i * math.sin(self.angle + i))
                color = (int((self.angle * 100 + i) % 255), int((self.angle * 50 + i) % 255), int((self.angle * 25 + i) % 255))
                pygame.draw.circle(self.screen, color, (x_pos, y_pos), 5)

        def update(self):
            self.angle += self.direction * self.speed
            self.arms = 100 + int(100 * math.sin(self.angle))

        def valmorphanize(self):
            self.direction *= -1  # Reverse the rotation direction
            self.speed *= 2  # Double the rotation speed

    class BouncingBalls:
        def __init__(self, screen):
            self.screen = screen
            self.balls = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), random.uniform(-4, 4), random.uniform(-4, 4), random.randint(10, 30), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1, random.choice([-1, 1])) for _ in range(20)]

        def draw(self):
            self.screen.fill((0, 0, 0))
            for x, y, _, _, radius, color, _, _ in self.balls:
                pygame.draw.circle(self.screen, color, (x, y), radius)
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), radius - 2)

        def update(self):
            new_balls = []
            for x, y, dx, dy, radius, color, size_oscillation, direction in self.balls:
                x += dx
                y += dy
                if x - radius <= 0 or x + radius >= WIDTH:
                    dx = -dx
                    color = tuple(min(255, c + 10) for c in color)
                if y - radius <= 0 or y + radius >= HEIGHT:
                    dy = -dy
                    color = tuple(min(255, c + 10) for c in color)

                # Oscillate the size of the ball with reduced magnitude and centered around the original size
                size_oscillation += 0.02 * direction
                if size_oscillation > 1.2 or size_oscillation < 0.8:
                    direction *= -1

                new_radius = max(10, int(radius * size_oscillation))

                # Smooth color transition
                r, g, b = color
                r = (r + random.randint(-2, 2)) % 256
                g = (g + random.randint(-2, 2)) % 256
                b = (b + random.randint(-2, 2)) % 256
                color = (r, g, b)

                new_balls.append((x, y, dx, dy, new_radius, color, size_oscillation, direction))
            self.balls = new_balls

        def valmorphanize(self):
            self.balls = [(x, y, random.uniform(-5, 5), random.uniform(-5, 5), random.randint(8, 32), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), size_oscillation, direction) for x, y, _, _, _, _, size_oscillation, direction in self.balls]

    class ZigZagPattern:
        def __init__(self, screen):
            self.screen = screen
            self.spacing = 20
            self.amplitude = 10
            self.frequency = 0.1
            self.speed = 0.05
            self.offset = 0
            self.color_shift = 0
            self.color = self.get_color(self.offset)
            self.direction = 1  # 1 for vertical, -1 for horizontal
            self.thickness = 2
            self.rotation_angle = 0

        def get_color(self, offset):
            """Generate a color based on the offset."""
            r = int(127.5 * (1 + math.sin(offset + self.color_shift)))
            g = int(127.5 * (1 + math.sin(offset + 2 * math.pi / 3 + self.color_shift)))
            b = int(127.5 * (1 + math.sin(offset + 4 * math.pi / 3 + self.color_shift)))
            return (r, g, b)

        def draw(self):
            for y in range(0, HEIGHT, self.spacing):
                points = []
                for x in range(0, WIDTH, 10):
                    if self.direction == 1:
                        points.append((x, y + self.amplitude * math.sin(self.frequency * x + self.offset)))
                    else:
                        points.append((y + self.amplitude * math.sin(self.frequency * y + self.offset), x))
                pygame.draw.lines(self.screen, self.color, False, points, self.thickness)

        def update(self):
            self.offset += self.speed
            self.color_shift += 0.01
            if self.offset > 2 * math.pi:
                self.reset_pattern()
            self.amplitude = 10 + 5 * math.sin(self.offset)
            self.spacing = int(20 + 10 * math.sin(0.5 * self.offset))
            self.frequency += 0.001
            self.thickness = int(2 + math.sin(self.offset))
            self.color = self.get_color(self.offset)
            if random.random() < 0.01:
                self.direction *= -1
            self.rotation_angle += 0.01

        def valmorphanize(self):
            self.reset_pattern()
            self.amplitude *= 2
            self.color = self.get_color(self.offset + math.pi / 2)
            self.direction *= -1
            self.rotation_angle += math.pi / 4

        def reset_pattern(self):
            self.offset = 0
            self.amplitude = 10
            self.frequency = 0.1
            self.speed = 0.05
            self.color = self.get_color(self.offset)


    class EKGPattern:
        def __init__(self, screen):
            self.screen = screen
            self.width, self.height = screen.get_size()
            self.points = []
            self.base_amplitude = 50
            self.frequency = 0.05
            self.speed = 5
            self.color = (255, 255, 255)
            self.x = 0
            self.y_offset = 0
            self.vertical_shift = 0
            self.max_vertical_shift = 50
            self.vertical_shift_direction = 1
            self.vertical_shift_speed = 2
            self.color_shift = 0
            self.grid_alpha = 255
            self.line_width = 1
            self.heartbeat_chance = 0.005
            self.bg_pulse = 0
            self.grid_size = 40
            self.grid_color_shift = 0

        def update(self):
            self.x += self.speed
            if self.x > self.width:
                self.x = 0
                self.points.clear()

            current_amplitude = self.base_amplitude + 10 * np.sin(0.01 * self.x)
            segment = len(self.points) % 250
            if segment < 60:
                self.y_offset = 0
            elif segment < 120:
                self.y_offset = current_amplitude * np.sin(self.frequency * self.x)
            elif segment < 180:
                self.y_offset = 0
            else:
                self.y_offset = -current_amplitude * 0.5 * np.sin(self.frequency * 0.5 * self.x + np.pi/4)

            self.vertical_shift += self.vertical_shift_speed * self.vertical_shift_direction
            if abs(self.vertical_shift) > self.max_vertical_shift:
                self.vertical_shift_direction *= -1

            y = self.height // 2 + self.y_offset + self.vertical_shift
            noise = np.random.randint(-5, 5)
            y += noise

            if np.random.random() < self.heartbeat_chance:
                self.y_offset += 3 * current_amplitude

            self.line_width = 1 + int(2 * np.sin(0.01 * self.x))
            self.points.append((self.x, y))

        def draw(self):
            self.bg_pulse += 0.01
            pulse_effect = 5 * np.sin(self.bg_pulse)
            for i in range(self.height):
                alpha = i / self.height
                color = (int(alpha * (10 + pulse_effect)), int(alpha * (10 + pulse_effect)), int(alpha * (15 + pulse_effect)))
                pygame.draw.line(self.screen, color, (0, i), (self.width, i))

            self.grid_size = 40 + int(10 * np.sin(0.01 * self.x))
            self.grid_color_shift += 0.01
            grid_hue = (self.grid_color_shift) % 1
            grid_color = pygame.Color(0)
            grid_color.hsla = (grid_hue * 360, 50, 25)  # Set HSL values
            grid_color.a = self.grid_alpha  # Set alpha value separately
            for i in range(0, self.width, self.grid_size):
                pygame.draw.line(self.screen, grid_color, (i, 0), (i, self.height))
            for i in range(0, self.height, self.grid_size):
                pygame.draw.line(self.screen, grid_color, (0, i), (self.width, i))

            self.color_shift += 0.01
            hue = (self.color_shift) % 1
            color = pygame.Color(0)
            color.hsla = (hue * 360, 70, 50, 100)

            if len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    fade_alpha = int(255 * (i / len(self.points)))
                    fade_color = (color.r, color.g, color.b, fade_alpha)
                    pygame.draw.line(self.screen, fade_color, self.points[i], self.points[i + 1], self.line_width)

        def valmorphanize(self):
            self.speed = np.random.choice([3, 4, 5, 6, 7])
            self.base_amplitude = np.random.choice([30, 40, 50, 60, 70])
            self.frequency *= np.random.choice([0.75, 1, 1.25, 1.5])
            self.vertical_shift_speed = np.random.choice([1, 2, 3])
            self.max_vertical_shift = np.random.choice([40, 50, 60, 70])


    class EtchASketch:
        def __init__(self, screen):
            self.screen = screen
            self.width, self.height = screen.get_size()
            self.color = (220, 220, 220)
            self.bg_color = (0, 0, 0)
            self.brush_x = 0
            self.brush_speed = self.width / 600
            self.horizon = int(self.height * 0.75)
            self.buildings = []
            self.clouds = [self.generate_cloud() for _ in range(5)]
            self.stars = [(np.random.randint(0, self.width), np.random.randint(0, self.horizon)) for _ in range(100)]
            self.moon_x = np.random.randint(50, self.width - 50)
            self.moon_y = np.random.randint(50, int(self.height * 0.5))
            self.moon_speed = 0.5
            self.moon_phase = np.random.choice(['full', 'crescent', 'half', 'gibbous'])



        def generate_cloud(self):
            x = np.random.randint(-100, self.width + 100)
            y = np.random.randint(50, self.horizon - 50)
            num_circles = np.random.randint(3, 6)
            circles = [(np.random.randint(x, x + 40), np.random.randint(y, y + 20), np.random.randint(15, 30)) for _ in range(num_circles)]
            speed = np.random.uniform(0.2, 0.5)
            return (circles, speed)

        def draw_sky_gradient(self):
            for i in range(self.height):
                alpha = i / self.height
                color = (int(alpha * 25), int(alpha * 25), int(alpha * 40))
                pygame.draw.line(self.screen, color, (0, i), (self.width, i))

        def draw_moon(self):
            color = (255, 255, 200)
            if self.moon_phase == 'full':
                pygame.draw.circle(self.screen, color, (int(self.moon_x), int(self.moon_y)), 30)
            elif self.moon_phase == 'crescent':
                pygame.draw.circle(self.screen, color, (int(self.moon_x), int(self.moon_y)), 30)
                pygame.draw.circle(self.screen, self.bg_color, (int(self.moon_x) + 10, int(self.moon_y)), 30)
            elif self.moon_phase == 'half':
                pygame.draw.circle(self.screen, color, (int(self.moon_x), int(self.moon_y)), 30)
                pygame.draw.circle(self.screen, self.bg_color, (int(self.moon_x) + 15, int(self.moon_y)), 30)
            elif self.moon_phase == 'gibbous':
                pygame.draw.circle(self.screen, color, (int(self.moon_x), int(self.moon_y)), 30)
                pygame.draw.circle(self.screen, self.bg_color, (int(self.moon_x) - 10, int(self.moon_y)), 30)

            for i in range(3):
                pygame.draw.circle(self.screen, (255, 255, 200), (int(self.moon_x), int(self.moon_y)), 30 + i * 5, 1)


        def draw_cloud(self, circles):
            for x, y, radius in circles:
                pygame.draw.circle(self.screen, (200, 200, 200), (int(x), int(y)), radius)

            # Cloud shadow
            for x, y, radius in circles:
                pygame.draw.circle(self.screen, (150, 150, 150), (int(x), int(y + 5)), radius)

        def draw_stars(self):
            for x, y in self.stars:
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1 if np.random.random() < 0.9 else 2)


        def draw(self):
            self.screen.fill(self.bg_color)
            self.draw_sky_gradient()
            self.draw_stars()
            for cloud in self.clouds:
                self.draw_cloud(cloud[0])
            self.draw_moon()

            # Draw the buildings created by the brush
            for x, y, width, height, building_color in self.buildings:
                pygame.draw.line(self.screen, building_color, (x, y), (x + width, y), 2)  # Top
                pygame.draw.line(self.screen, building_color, (x, y), (x, y + height), 2)  # Left
                pygame.draw.line(self.screen, building_color, (x + width, y), (x + width, y + height), 2)  # Right

                # Draw windows on the buildings
                for wx in range(int(x) + 5, int(x + width), 10):
                    for wy in range(int(y) + 5, int(y + height), 15):
                        if np.random.random() < 0.7:
                            pygame.draw.rect(self.screen, (255, 255, 0), (wx, wy, 5, 10))

            pygame.display.flip()

        def update(self):
            # Brush logic to draw buildings
            building_width = np.random.randint(30, 100)
            building_height = np.random.randint(50, self.height - self.horizon)
            building_color = tuple(np.clip(np.array(self.color) + np.random.randint(-20, 20, 3), 0, 255))

            # Adjust the brush movement speed
            self.brush_x += self.brush_speed
            if self.brush_x < self.width:
                self.buildings.append((self.brush_x, self.horizon - building_height, building_width, building_height, building_color))
            else:
                self.brush_x = 0
                self.buildings.clear()

            # Update moon position
            self.moon_x += self.moon_speed
            if self.moon_x > self.width + 30:
                self.moon_x = -30

            # Update cloud positions
            new_clouds = []
            for circles, speed in self.clouds:
                new_circles = [(x + speed, y, radius) for x, y, radius in circles]
                if new_circles[0][0] > self.width + 100:
                    new_clouds.append(self.generate_cloud())
                else:
                    new_clouds.append((new_circles, speed))
            self.clouds = new_clouds

        def valmorphanize(self):
            # Randomly change the brush speed
            self.brush_speed = np.random.uniform(self.width / 800, self.width / 400)

            # Randomly change the moon phase and speed
            self.moon_phase = np.random.choice(['full', 'crescent', 'half', 'gibbous'])
            self.moon_speed = np.random.uniform(0.3, 0.7)

            # Randomly change the building color
            self.color = (np.random.randint(150, 255), np.random.randint(150, 255), np.random.randint(150, 255))

            # Randomly change the background color
            self.bg_color = (np.random.randint(0, 50), np.random.randint(0, 50), np.random.randint(0, 50))

            # Randomly regenerate clouds
            self.clouds = [self.generate_cloud() for _ in range(np.random.randint(3, 7))]
    class LissajousCurve:
        def __init__(self, screen):
            self.screen = screen
            self.width, self.height = screen.get_size()
            self.num_lines = 3
            self.paths = [[] for _ in range(self.num_lines)]
            self.current_indices = [0 for _ in range(self.num_lines)]
            self.speeds = [0.01 for _ in range(self.num_lines)]
            self.as_values = [3, 4, 5]
            self.bs_values = [2, 3, 4]
            self.deltas = [np.pi / 2, np.pi / 3, np.pi / 4]
            self.zoom = 1.0
            self.line_thickness = 5
            self.colors = [(220, 220, 220), (220, 150, 150), (150, 220, 150)]
            self.bg_color = (0, 0, 0)
            self.fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.fade_surface.fill((0, 0, 0, 10))

        def draw(self):
            self.screen.fill(self.bg_color)
            for i in range(self.num_lines):
                if len(self.paths[i]) > 1:
                    pygame.draw.lines(self.screen, self.colors[i], False, self.paths[i], self.line_thickness)
            self.screen.blit(self.fade_surface, (0, 0))
            pygame.display.flip()

        def update(self):
            for i in range(self.num_lines):
                t = self.current_indices[i]
                x = int(self.width / 2 + self.zoom * self.width / 4 * np.sin(self.as_values[i] * t + self.deltas[i]))
                y = int(self.height / 2 + self.zoom * self.height / 4 * np.sin(self.bs_values[i] * t))
                self.paths[i].append((x, y))
                self.current_indices[i] += self.speeds[i]
                if len(self.paths[i]) > 500:
                    self.paths[i].pop(0)

        def valmorphanize(self):
            for i in range(self.num_lines):
                self.as_values[i] += np.random.choice([-1, 1])
                self.bs_values[i] += np.random.choice([-1, 1])
                self.deltas[i] += np.random.uniform(-0.1, 0.1)
                self.speeds[i] = np.random.uniform(0.005, 0.02)
                self.colors[i] = (np.random.randint(150, 255), np.random.randint(150, 255), np.random.randint(150, 255))
            self.bg_color = (np.random.randint(0, 50), np.random.randint(0, 50), np.random.randint(0, 50))

    class PerlinFlowField:
        class Particle:
            def __init__(self, x, y, screen_width, screen_height):
                self.x = x
                self.y = y
                self.screen_width = screen_width
                self.screen_height = screen_height
                self.color = (np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255))
                self.speed = 2
                self.vel = np.array([0, 0])  # Initialize velocity

            def update(self, angle):
                # Update the particle's position based on its velocity
                self.x += self.speed * np.cos(angle)
                self.y += self.speed * np.sin(angle)

                # Wrap around the screen if the particle goes out of bounds
                self.x %= self.screen_width
                self.y %= self.screen_height


        def __init__(self, screen):
            self.screen = screen
            self.width, self.height = screen.get_size()

            # 1. Reduce the number of particles to half
            self.particles = [self.Particle(np.random.randint(0, self.width), np.random.randint(0, self.height), self.width, self.height) for _ in range(250)]

            self.flowfield_resolution = 10
            self.noise_scale = 0.1
            self.color_shift = 0
            self.circle_size = 3  # Default circle size

            # 2. Define a limited color palette
            self.color_palette = [
                (255, 0, 0),  # Red
                (0, 255, 0),  # Green
                (0, 0, 255),  # Blue
                (255, 255, 0),  # Yellow
                (0, 255, 255),  # Cyan
            ]

        def draw(self):
            # Fade effect
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 2))  # The last value is the alpha channel (transparency)
            self.screen.blit(overlay, (0, 0))

            # Update particles
            for particle in self.particles:
                # Get noise value based on particle's position
                noise_val = noise.pnoise2(particle.x * self.noise_scale,
                                        particle.y * self.noise_scale,
                                        octaves=3,
                                        persistence=0.5,
                                        lacunarity=2.0,
                                        repeatx=self.width,
                                        repeaty=self.height,
                                        base=42)

                # Convert noise value to angle
                angle = noise_val * 2 * np.pi

                # Update particle's velocity and position based on angle
                particle.update(angle)

                 # Use colors from the limited palette
                color = self.color_palette[int((angle + self.color_shift) % len(self.color_palette))]
                pygame.draw.circle(self.screen, color, (int(particle.x), int(particle.y)), self.circle_size)

                # Respawn particle if it goes off screen
                if particle.x < 0 or particle.x > self.width or particle.y < 0 or particle.y > self.height:
                    particle.x = np.random.randint(0, self.width)
                    particle.y = np.random.randint(0, self.height)
                    particle.prev_pos = np.array([particle.x, particle.y])

            # Gradually change color
            self.color_shift += 0.005

            pygame.display.flip()

        def valmorphanize(self):
            # Randomly adjust the particle speed
            self.particles_speed_factor = np.random.choice([0.5, 1, 1.5, 2])
            for particle in self.particles:
                particle.speed *= self.particles_speed_factor

            # Randomly adjust the noise scale
            self.noise_scale = np.random.choice([0.05, 0.1, 0.15, 0.2])

            # Randomly adjust the circle size
            self.circle_size = np.random.randint(2, 6)
    class MandalaPattern:
        def __init__(self, screen):
            self.screen = screen
            self.reset_fractal()

        def reset_fractal(self):
            self.center = (WIDTH // 2, HEIGHT // 2)
            self.radius = 50
            self.angle = 0
            self.rotation_angle = 0
            self.circle_rotation_angle = 0
            self.arc_length = math.pi / 6
            self.line_color = (235, 235, 235)  # Light color for lines
            self.num_symmetrical_lines = 24
            self.bg_color = (10, 10, 10)  # Very dark background color
            self.petals_radius = 10
            self.line_width = 1

        def draw_groovy_background(self):
            gradient_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            gradient_surface.fill((*self.bg_color, 15))
            self.screen.blit(gradient_surface, (0, 0))

        def draw_centered_petals(self):
            for i in range(self.num_symmetrical_lines):
                angle_offset = (2 * math.pi / self.num_symmetrical_lines) * i
                end_pos = (
                    self.center[0] + self.petals_radius * math.cos(self.angle + angle_offset + self.rotation_angle),
                    self.center[1] + self.petals_radius * math.sin(self.angle + angle_offset + self.rotation_angle)
                )
                pygame.draw.line(self.screen, self.line_color, self.center, end_pos, self.line_width)
            self.petals_radius += 2
            if self.petals_radius > WIDTH // 4:
                self.petals_radius = 10

        def draw_rotating_circles(self):
            for i in range(self.num_symmetrical_lines):
                angle_offset = (2 * math.pi / self.num_symmetrical_lines) * i
                start_pos = (
                    self.center[0] + self.radius * math.cos(self.angle + angle_offset + self.rotation_angle),
                    self.center[1] + self.radius * math.sin(self.angle + angle_offset + self.rotation_angle)
                )
                end_pos = (
                    self.center[0] + self.radius * math.cos(self.angle + angle_offset + self.rotation_angle + self.arc_length),
                    self.center[1] + self.radius * math.sin(self.angle + angle_offset + self.rotation_angle + self.arc_length)
                )
                pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, self.line_width)

        def draw(self):
            self.draw_groovy_background()
            self.draw_rotating_circles()
            self.draw_centered_petals()
            self.radius += 0.5
            self.rotation_angle += 0.02
            self.circle_rotation_angle += 0.01
            self.arc_length += 0.001
            self.line_width = 1 + int(self.radius) % 3  # Varying line width
            if self.arc_length > math.pi / 3 or self.arc_length < math.pi / 6:
                self.arc_length = math.pi / 6
            if self.radius > WIDTH // 2:
                self.reset_fractal()


        def update(self):
            self.line_color = ((self.line_color[0] + 1) % 230, (self.line_color[1] + 1) % 230, (self.line_color[2] + 1) % 230)

        def valmorphanize(self):
            self.radius = 50
            self.line_color = (random.randint(180, 220), random.randint(180, 220), random.randint(180, 220))
            self.angle_step = 0.0005
            self.reset_fractal()

    class BioluminescentForest:
        def __init__(self, screen):
            self.screen = screen
            self.bg_color = (10, 10, 10)
            self.tree_base_color = (50, 255, 50)
            self.particle_color = (255, 255, 255)
            self.num_trees = 10
            self.num_particles = 100
            self.trees = []
            self.particles = []
            self.initialize_forest()

        def initialize_forest(self):
            for _ in range(self.num_trees):
                x = random.randint(0, WIDTH)
                y = random.randint(HEIGHT // 2, HEIGHT)
                height = random.randint(50, 150)
                branches = [random.uniform(0.6, 1.4) for _ in range(3)]
                self.trees.append((x, y, height, branches))

            for _ in range(self.num_particles):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                speed = random.uniform(0.5, 2)
                size = random.randint(1, 3)
                self.particles.append([x, y, speed, size])

        def draw_background(self, color_intensity):
            gradient = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(HEIGHT):
                alpha = int(255 * (i / HEIGHT) * color_intensity)
                gradient.fill((self.bg_color[0], self.bg_color[1], self.bg_color[2], alpha), rect=(0, i, WIDTH, 1))
            self.screen.blit(gradient, (0, 0))

        def draw_trees(self, zoom_level, rotation_angle):
            for x, y, height, branches in self.trees:
                adjusted_height = int(height * zoom_level)
                tree_color = (int(self.tree_base_color[0] * zoom_level), int(self.tree_base_color[1] * zoom_level), int(self.tree_base_color[2] * zoom_level))
                pygame.draw.line(self.screen, tree_color, (x, y), (x, y - adjusted_height), 2)
                branch_length = adjusted_height // 3
                for i, branch_factor in enumerate(branches):
                    angle = rotation_angle + (math.pi / 6 * i * branch_factor)
                    end_x = x + branch_length * math.cos(angle)
                    end_y = y - (i + 1) * branch_length * math.sin(angle)
                    pygame.draw.line(self.screen, tree_color, (x, y - i * branch_length), (end_x, end_y), 2)

        def draw_particles(self, pattern_density):
            for particle in self.particles:
                x, y, speed, size = particle
                pygame.draw.circle(self.screen, self.particle_color, (int(x), int(y)), size)
                particle[1] -= speed
                particle[0] += random.uniform(-0.5, 0.5)  # Slight horizontal movement
                if y < 0:
                    particle[1] = HEIGHT
                    particle[0] = random.randint(0, WIDTH)
                    particle[2] = random.uniform(0.5, 2 * pattern_density)
                    particle[3] = random.randint(1, 3)

        def draw(self, zoom_level=1, rotation_angle=0, color_intensity=0, pattern_density=0):
            self.draw_background(color_intensity)
            self.draw_trees(zoom_level, rotation_angle)
            self.draw_particles(pattern_density)

        def update(self):
            pass

        def valmorphanize(self):
            self.initialize_forest()
