import pygame
import numpy as np
import random
import colorsys

# Constants
WIDTH, HEIGHT = 800, 600
REDUCED_WIDTH, REDUCED_HEIGHT = 256, 256

class VisualEngine:
    def valmorphanize(self):
        """Default Valmorphanize effect. Can be overridden by subclasses."""
        pass

    # Class for a Basic Fractal
    class FractalA:
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

    class FractalB:
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

    class FractalC:
        def __init__(self, screen):
            self.screen = screen
            self.dt = 0.01
            self.sigma = 10.0
            self.beta = 8.0 / 3.0
            self.rho = 28.0
            self.x, self.y, self.z = 0.1, 0, 0
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.bg_color = (0, 0, 0)
            self.points = []

        def draw(self):
            self.screen.fill(self.bg_color)
            for point in self.points:
                pygame.draw.circle(self.screen, self.color, (int(point[0]), int(point[1])), 1)

        def update(self):
            dx = self.sigma * (self.y - self.x) * self.dt
            dy = (self.x * (self.rho - self.z) - self.y) * self.dt
            dz = (self.x * self.y - self.beta * self.z) * self.dt

            self.x += dx
            self.y += dy
            self.z += dz

            # Scale and translate the points for visualization
            px = int((self.x + 30) * (WIDTH / 60))
            py = int((self.y + 30) * (HEIGHT / 60))

            self.points.append((px, py))
            if len(self.points) > 10000:  # Keep the last 10000 points for performance
                self.points.pop(0)

        def valmorphanize(self):
            # change parameters
            self.sigma = random.uniform(0, 50)
            self.beta = random.uniform(0, 10)
            self.rho = random.uniform(0, 50)
            # change color
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


    class Spirograph:
        def __init__(self, screen):
            self.screen = screen
            self.t = 0
            self.R = 125
            self.r = 75
            self.l = 0.8
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.bg_color = (0, 0, 0)
            self.points = []

        def draw(self):
            self.screen.fill(self.bg_color)
            for point in self.points:
                pygame.draw.circle(self.screen, self.color, (int(point[0]), int(point[1])), 1)

        def update(self):
            x = (self.R + self.r) * np.cos(self.t) - self.l * self.r * np.cos((self.R + self.r) * self.t / self.r)
            y = (self.R + self.r) * np.sin(self.t) - self.l * self.r * np.sin((self.R + self.r) * self.t / self.r)

            # Translate the points for visualization
            px = int(x + WIDTH / 2)
            py = int(y + HEIGHT / 2)

            self.points.append((px, py))
            self.t += 0.05

            if len(self.points) > 5000:  # Keep the last 5000 points for performance
                self.points.pop(0)

        def valmorphanize(self):
            # Change the radius of the larger circle, R
            self.R = random.uniform(100, 150)
            # Change the radius of the smaller circle, r
            self.r = random.uniform(50, 100)
            # Change the l factor which affects the shape of the curve
            self.l = random.uniform(0.5, 1.0)
            # Generate a new random color
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            # Empty the list of drawn points
            self.points.clear()
            # Reset time parameter
            self.t = 0


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
            self.max_circles = 5
            self.angles = [random.uniform(0, 2 * np.pi) for _ in range(self.max_circles)]
            self.radii = [random.randint(40, 90) for _ in range(self.max_circles)]
            self.speeds = [random.uniform(0.02, 0.05) for _ in range(self.max_circles)]
            self.color_angle = 0
            self.pulse_direction = 1
            self.bg_hue = random.randint(0, 360)
            self.time = 0
            self.max_circle_size = 10
            self.pulse_frequency = 20
            self.thickness_factor = 1

        def draw_gradient_background(self):
            top_color = pygame.Color(0)
            bottom_color = pygame.Color(0)
            top_color.hsva = (self.bg_hue % 360, 70, 90, 100)
            bottom_color.hsva = ((self.bg_hue + 180) % 360, 70, 50, 100)

            for y in range(HEIGHT):
                blend = y / HEIGHT
                color = top_color.lerp(bottom_color, blend)
                pygame.draw.line(self.screen, color, (0, y), (WIDTH, y))

        def draw(self):
            self.draw_gradient_background()

            for i in range(len(self.angles)):
                for _ in range(10):  # Draw 10 circles in each frame for denser patterns
                    x = WIDTH // 2 + self.radii[i] * np.cos(self.angles[i])
                    y = HEIGHT // 2 + self.radii[i] * np.sin(self.angles[i])

                    color = pygame.Color(0)
                    hue_variation = int(30 * np.sin(self.time + i))
                    color.hsva = ((self.color_angle + hue_variation) % 360, 100, 100, 100)

                    circle_size = int(5 * self.thickness_factor * (1 - self.radii[i] / (max(WIDTH, HEIGHT) * 0.7)))
            # Draw the circle
                    pygame.draw.circle(self.screen, color, (int(x), int(y)), circle_size)

                    self.angles[i] += self.speeds[i]
                    self.radii[i] += self.pulse_frequency * np.sin(self.time)  # Dynamic radius change based on sine wave
                    self.color_angle += 1

                    # Reset radii if they exceed a threshold
                    if self.radii[i] > max(WIDTH, HEIGHT) * 0.7:
                        self.radii[i] = random.randint(40, 90)
                        self.speeds[i] = random.uniform(0.02, 0.05)

            self.bg_hue += 0.5  # Slowly change the hue for the gradient background
            self.time += 0.01  # Increment time for dynamic effects

        def update(self):
            pass  # No specific update logic for this fractal

        def valmorphanize(self):
            # Randomly choose to increase or decrease thickness
            boost_or_reduce = random.choice([1.5, 0.7])  # < 1 to reduce, > 1 to boost

            self.thickness_factor *= boost_or_reduce

            # Add some constraints to keep thickness factor within reasonable limits
            self.thickness_factor = max(min(self.thickness_factor, 2), 0.5)

            # Keep radii within screen limits
            self.radii = [min(radius, min(WIDTH, HEIGHT) / 3) for radius in self.radii]


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
