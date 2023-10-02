import pygame
import pygame_gui
from visual_engine import VisualEngine
from audio_engine import AudioEngine
from ui_elements import Button, MuteButton

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

    # Dynamically fetch all audio mode classes inside AudioEngine
    audio_mode_classes = [cls for name, cls in AudioEngine.__dict__.items() if isinstance(cls, type) and issubclass(cls, AudioEngine.BaseAudioMode) and cls is not AudioEngine.BaseAudioMode]
    audio_mode_names = [cls.__name__ for cls in audio_mode_classes]

    # Check if audio_mode_names is not empty
    if not audio_mode_names:
        raise ValueError("No audio modes found!")

    # Instantiate AudioEngine
    audio_engine = AudioEngine()
    default_mode = AudioEngine.DefaultAudioMode(audio_engine=audio_engine)


    # Dynamically fetch all fractal classes inside VisualEngine
    fractal_classes = [cls for name, cls in VisualEngine.__dict__.items() if isinstance(cls, type)]
    fractal_names = [cls.__name__ for cls in fractal_classes]

    # Initialize all fractals
    fractals = {name: cls(screen) for name, cls in zip(fractal_names, fractal_classes)}
    current_fractal = fractals[fractal_names[0]]  # Default to the first fractal

    # -- Dropdown Menu setup
    drop_down_menu = pygame_gui.elements.UIDropDownMenu(fractal_names, fractal_names[0], pygame.Rect((10, 10), (150, 30)), manager)
    audio_drop_down_menu = pygame_gui.elements.UIDropDownMenu(audio_mode_names, audio_mode_names[0], pygame.Rect((170, 10), (150, 30)), manager)


    # Button setup
    quit_button = Button(WIDTH - 110, HEIGHT - 60, 100, 40, "Quit", (255, 0, 0))
    valmorphanize_button = Button(VALMORPHANIZE_BUTTON_X, VALMORPHANIZE_BUTTON_Y, VALMORPHANIZE_BUTTON_WIDTH, VALMORPHANIZE_BUTTON_HEIGHT, "Valmorphanize", (0, 255, 0))
    mute_button = MuteButton(WIDTH-220, HEIGHT-60, 100, 40, "Mute", (255, 0, 0), (150, 150, 150), audio_engine=audio_engine)


    while running:
        time_delta = clock.tick(30)/1000.0  # Add the time_delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                # Handle audio dropdown selection
                if event.ui_element == audio_drop_down_menu:
                    selected_audio_mode = event.text
                    audio_engine.mode = audio_mode_classes[audio_mode_names.index(selected_audio_mode)](audio_engine=audio_engine)

                # Handle visual dropdown selection
                elif event.ui_element == drop_down_menu:
                    selected_visual_mode = event.text
                    current_fractal = fractals[selected_visual_mode]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_over(pygame.mouse.get_pos()):
                    running = False
                if valmorphanize_button.is_over(pygame.mouse.get_pos()):
                    current_fractal.valmorphanize()
                if mute_button.is_over(pygame.mouse.get_pos()):
                    mute_button.toggle_mute()


        # Update and draw fractal
        if hasattr(current_fractal, 'update'):
            current_fractal.update()
        current_fractal.draw()

        # Generate and play sound
        audio_parameters = current_fractal.get_audio_parameters()
        sound = audio_engine.generate_tone_with_envelope(audio_parameters)
        audio_engine.play_sound(sound)

        # Draw the button after the fractal
        quit_button.draw(screen)
        valmorphanize_button.draw(screen)
        mute_button.draw(screen)

        # Update and draw the UI
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
