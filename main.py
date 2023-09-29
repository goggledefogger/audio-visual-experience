import pygame
from visual_engine import VisualEngine
from audio_engine import AudioEngine
from ui_elements import Button

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Audio-Visual Experience')

def main():
    clock = pygame.time.Clock()
    running = True

    visual_engine = VisualEngine(screen)
    audio_engine = AudioEngine()

    # Button setup
    quit_button = Button(WIDTH - 110, 10, 100, 40, "Quit", (255, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_over(pygame.mouse.get_pos()):
                    running = False

        # Update and draw fractal
        visual_engine.update()
        visual_engine.draw_fractal()

        # Draw the button after the fractal
        quit_button.draw(screen)

        # Generate and play sound
        sound = audio_engine.generate_tone_with_envelope(visual_engine.zoom)
        audio_engine.play_sound(sound)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
