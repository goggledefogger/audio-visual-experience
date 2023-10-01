import pygame
import numpy as np
import random
import colorsys
import math
import noise

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
            self.bg_color = (0, 0, 0)
            self.spirographs = [self._create_spirograph() for _ in range(3)]  # Create 3 spirographs

        def _create_spirograph(self):
            R = random.randint(50, 150)
            r = random.randint(25, 125)
            l = random.uniform(0.5, 1.0)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            return {"R": R, "r": r, "l": l, "color": color, "points": []}

        def draw(self):
            self.screen.fill(self.bg_color)
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

        def valmorphanize(self):
            for spiro in self.spirographs:
                # Change base hue slightly and increase saturation to give a boosted feel
                h, s, v = colorsys.rgb_to_hsv(*spiro["color"])
                h = (h + random.uniform(-0.1, 0.1)) % 1.0  # slight change in hue
                s = min(1, s + random.uniform(0.1, 0.3))  # increase saturation but don't exceed 1
                spiro['color'] = colorsys.hsv_to_rgb(h, s, v)

            # Boost the time change slightly (equivalent to speed) for more rapid transformations
            self.t += (0.05 + random.uniform(0.05, 0.2)) # increase the change in time step to make the transitions faster



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
            self.max_circles = random.randint(3, 7)  # Variable number of circles
            self.angles = [random.uniform(0, 2 * np.pi) for _ in range(self.max_circles)]
            self.radii = [random.randint(20, min(self.width, self.height) // 6) for _ in range(self.max_circles)]
            self.speeds = [random.uniform(0.01, 0.04) for _ in range(self.max_circles)]
            self.color_angle = 0
            self.bg_hue = random.randint(0, 360)
            self.time = 0
            self.pulse_frequency = random.uniform(5, 20)
            self.thickness_factor = 1
            self.pulse_direction = random.choice([-1, 1])
            self.start_x = random.randint(self.width // 4, 3 * self.width // 4)  # Dynamic starting point
            self.start_y = random.randint(self.height // 4, 3 * self.height // 4)  # Dynamic starting point
            self.bg_pulse = 0

        def draw_gradient_background(self):
            top_color = pygame.Color(0)
            bottom_color = pygame.Color(0)
            top_color.hsva = ((self.bg_hue + int(10 * np.sin(self.bg_pulse))) % 360, 50, 85, 100)  # Background pulse
            bottom_color.hsva = ((self.bg_hue + 180 + int(10 * np.sin(self.bg_pulse))) % 360, 50, 65, 100)  # Background pulse

            for y in range(self.height):
                blend = y / self.height
                color = top_color.lerp(bottom_color, blend)
                pygame.draw.line(self.screen, color, (0, y), (self.width, y))


        def draw(self):
            self.draw_gradient_background()

            for i in range(len(self.angles)):
                for _ in range(10):  # Draw 10 circles in each frame for denser patterns
                    x = self.start_x + self.radii[i] * np.cos(self.angles[i])
                    y = self.start_y + self.radii[i] * np.sin(self.angles[i])

                    color = pygame.Color(0)
                    hue_variation = int(30 * np.sin(self.time + i))
                    color.hsva = ((self.color_angle + hue_variation) % 360, 60, 80, 100)  # Reduced saturation and adjusted value for softer colors

                    circle_size = int(3 * self.thickness_factor * (1 + np.sin(self.time)))  # Dynamic circle size based on sine wave
                    pygame.draw.circle(self.screen, color, (int(x), int(y)), circle_size)

                    self.angles[i] += self.speeds[i]
                    self.radii[i] += self.pulse_frequency * np.sin(self.time)  # Dynamic radius change based on sine wave

                    # Reset radii if they exceed a threshold to keep them on screen
                    if self.radii[i] > min(self.width, self.height) // 3:  # Adjusted threshold
                        self.radii[i] = random.randint(20, min(self.width, self.height) // 6)
                        self.speeds[i] = random.uniform(0.01, 0.04)

                self.bg_hue += 0.5  # Slowly change the hue for the gradient background
                self.time += 0.01  # Increment time for dynamic effects


        def update(self):
            self.bg_pulse += 0.01  # Increment for background pulse


        def valmorphanize(self):
            # Randomly choose to increase or decrease thickness
            boost_or_reduce = random.choice([1.5, 0.7])  # < 1 to reduce, > 1 to boost

            self.thickness_factor *= boost_or_reduce

            # Add some constraints to keep thickness factor within reasonable limits
            self.thickness_factor = max(min(self.thickness_factor, 2), 0.5)

            # Keep radii within screen limits
            self.radii = [min(radius, min(WIDTH, HEIGHT) / 3) for radius in self.radii]

            # Occasionally add or remove circles for complexity
            if random.random() < 0.1 and len(self.angles) < 7:
                self.angles.append(random.uniform(0, 2 * np.pi))
                self.radii.append(random.randint(40, 90))
                self.speeds.append(random.uniform(0.02, 0.05))
            elif random.random() < 0.1 and len(self.angles) > 3:
                index_to_remove = random.randint(0, len(self.angles) - 1)
                self.angles.pop(index_to_remove)
                self.radii.pop(index_to_remove)
                self.speeds.pop(index_to_remove)

            # Randomize pulse direction
            self.pulse_direction = random.choice([-1, 1])

             # Randomize spirograph speeds
            self.speeds = [random.uniform(0.01, 0.06) for _ in range(len(self.speeds))]

            # Randomize starting positions
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
            # Dynamic gradient background
            for y in range(HEIGHT):
                blend = y / HEIGHT
                color = self.bg_color1.lerp(self.bg_color2, blend)
                pygame.draw.line(self.screen, color, (0, y), (WIDTH, y))

            # Adjust max_dots dynamically
            self.max_dots = int(400 + 100 * np.sin(self.time))

            # Add new dots
            while len(self.dots) < self.max_dots:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.uniform(1, 3)
                growth_rate = random.uniform(0.1, 0.3) * random.choice([1, -1])  # Increased growth rate
                hue = (x + y + int(200 * np.sin(self.time))) % 360
                color = pygame.Color(0)
                color.hsva = (hue, 100, 100, random.randint(50, 100))  # Randomized opacity
                dx = random.uniform(-1, 1)  # Increased movement speed
                dy = random.uniform(-1, 1)  # Increased movement speed
                self.dots.append([x, y, size, growth_rate, color, dx, dy])

            # Draw and update dots
            for dot in self.dots:
                pygame.draw.circle(self.screen, dot[4], (dot[0], dot[1]), int(dot[2]))
                dot[2] += dot[3]
                dot[0] += dot[5]
                dot[1] += dot[6]

                if dot[2] > 20 or dot[2] < 1 or dot[0] < 0 or dot[0] > WIDTH or dot[1] < 0 or dot[1] > HEIGHT:
                    self.dots.remove(dot)

            self.time += 0.02  # Increased time increment

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
            # Add a new attribute for valmorphanize effect duration
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
            return tuple(int(a * (1 - alpha) + b * alpha) for a, b in zip(color1, color2))

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
                    hex_size = base_hex_size + 15 * np.sin(2 * self.time + row + col)  # Faster size modulation
                    x = col * np.sqrt(3) * base_hex_size * self.zoom_factor + self.pan_x
                    y = row * 1.5 * base_hex_size * self.zoom_factor + self.pan_y
                    if col % 2 == 1:
                        y += 0.75 * base_hex_size * self.zoom_factor
                    color_idx = (row + col) % 8
                    next_color_idx = (color_idx + 1) % 8
                    color = self.lerp_color(self.palette[color_idx], self.palette[next_color_idx], alpha)
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
            self.angle += 0.01  # Faster rotation
            self.time += 0.005  # Faster color transition

            # Dynamic zooming
            self.zoom_factor += 0.005 * self.zoom_direction
            if self.zoom_factor > 1.2 or self.zoom_factor < 0.8:
                self.zoom_direction *= -1

            # Panning effect
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
            # Change the base hue and generate a new palette
            self.base_hue = random.random()
            self.palette = self.generate_palette()

            # Invert and augment the angle for drastic change (0 for no rotation, 3.14 for inverted)
            self.angle = 3.14 if random.random() > 0.5 else 0

            # Change pan direction
            self.pan_speed_x *= random.choice([-1, 1])
            self.pan_speed_y *= random.choice([-1, 1])

            # Change Time drastically
            self.time = random.uniform(0, 10)

            # Change Zoom factor
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
            self.color = self.get_color(self.offset)
            self.direction = 1  # 1 for vertical, -1 for horizontal
            self.thickness = 2

        def get_color(self, offset):
            """Generate a color based on the offset."""
            r = int(127.5 * (1 + math.sin(offset)))
            g = int(127.5 * (1 + math.sin(offset + 2 * math.pi / 3)))
            b = int(127.5 * (1 + math.sin(offset + 4 * math.pi / 3)))
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
            if self.offset > 2 * math.pi:
                self.reset_pattern()
            self.amplitude = 10 + 5 * math.sin(self.offset)
            self.spacing = int(20 + 10 * math.sin(0.5 * self.offset))
            self.frequency += 0.001
            self.thickness = int(2 + math.sin(self.offset))
            self.color = self.get_color(self.offset)
            if random.random() < 0.01:
                self.direction *= -1

        def valmorphanize(self):
            self.reset_pattern()
            self.amplitude *= 2
            self.color = self.get_color(self.offset + math.pi / 2)
            self.direction *= -1

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

        def update(self):
            self.x += self.speed
            if self.x > self.width:
                self.x = 0
                self.points.clear()

            # Dynamic amplitude
            current_amplitude = self.base_amplitude + 10 * np.sin(0.01 * self.x)

            # Enhanced EKG waveform logic with added complexity
            segment = len(self.points) % 250
            if segment < 60:
                self.y_offset = 0
            elif segment < 120:
                self.y_offset = current_amplitude * np.sin(self.frequency * self.x)
            elif segment < 180:
                self.y_offset = 0
            else:
                self.y_offset = -current_amplitude * 0.5 * np.sin(self.frequency * 0.5 * self.x + np.pi/4)

            # Vertical shift logic
            self.vertical_shift += self.vertical_shift_speed * self.vertical_shift_direction
            if abs(self.vertical_shift) > self.max_vertical_shift:
                self.vertical_shift_direction *= -1

            y = self.height // 2 + self.y_offset + self.vertical_shift
            self.points.append((self.x, y))

        def draw(self):
            # Dynamic background gradient
            for i in range(self.height):
                alpha = i / self.height
                color = (int(alpha * 10), int(alpha * 10), int(alpha * 15))
                pygame.draw.line(self.screen, color, (0, i), (self.width, i))

            # Dynamic grid fade in/out
            self.grid_alpha += self.vertical_shift_direction * 5
            self.grid_alpha = max(0, min(255, self.grid_alpha))
            grid_color = (15, 15, 15, self.grid_alpha)

            for i in range(0, self.width, 40):
                pygame.draw.line(self.screen, grid_color, (i, 0), (i, self.height))
            for i in range(0, self.height, 40):
                pygame.draw.line(self.screen, grid_color, (0, i), (self.width, i))

            # Color transition
            self.color_shift += 0.01
            hue = (self.color_shift) % 1
            color = pygame.Color(0)
            color.hsla = (hue * 360, 100, 50, 100)

            if len(self.points) > 1:
                pygame.draw.aalines(self.screen, color, False, self.points)

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

