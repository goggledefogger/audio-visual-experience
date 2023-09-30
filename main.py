import pygame
import pygame_gui
from visual_engine import VisualEngine
from audio_engine import AudioEngine
from ui_elements import Button

# Constants
WIDTH, HEIGHT = 800, 600

VALMORPHANIZE_BUTTON_WIDTH = 150
VALMORPHANIZE_BUTTON_HEIGHT = 40
VALMORPHANIZE_BUTTON_X = WIDTH - VALMORPHANIZE_BUTTON_WIDTH - 10
VALMORPHANIZE_BUTTON_Y = 60

# Colors
WHITE = (255, 255, 255)


# Initialize pygame
pygame.init()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # Initialize UI Manager

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Audio-Visual Experience')

def main():
    clock = pygame.time.Clock()
    running = True

    audio_engine = AudioEngine()

    # Dynamically fetch all fractal classes inside VisualEngine
    fractal_classes = [cls for name, cls in VisualEngine.__dict__.items() if isinstance(cls, type)]
    fractal_names = [cls.__name__ for cls in fractal_classes]

    # Initialize all fractals
    fractals = {name: cls(screen) for name, cls in zip(fractal_names, fractal_classes)}
    current_fractal = fractals[fractal_names[0]]  # Default to the first fractal

    # -- Dropdown Menu setup
    drop_down_menu = pygame_gui.elements.UIDropDownMenu(fractal_names, fractal_names[0], pygame.Rect((10, 10), (150, 30)), manager)

    # Button setup
    quit_button = Button(WIDTH - 110, 10, 100, 40, "Quit", (255, 0, 0))
    valmorphanize_button = Button(VALMORPHANIZE_BUTTON_X, VALMORPHANIZE_BUTTON_Y, VALMORPHANIZE_BUTTON_WIDTH, VALMORPHANIZE_BUTTON_HEIGHT, "Valmorphanize", (0, 255, 0))

    while running:
        time_delta = clock.tick(30)/1000.0  # Add the time_delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    current_fractal = fractals[drop_down_menu.selected_option]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_over(pygame.mouse.get_pos()):
                    running = False
                if valmorphanize_button.is_over(pygame.mouse.get_pos()):
                    current_fractal.valmorphanize()


        # Update and draw fractal
        current_fractal.update()
        current_fractal.draw()

        # Generate and play sound
        zoom_value = getattr(current_fractal, 'zoom', 1)  # Use zoom if available, else default to 1
        sound = audio_engine.generate_tone_with_envelope(zoom_value)
        audio_engine.play_sound(sound)

        # Draw the button after the fractal
        quit_button.draw(screen)
        valmorphanize_button.draw(screen)

        # Update and draw the UI
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
