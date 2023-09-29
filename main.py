import pygame
from visual_engine import VisualEngine
from audio_engine import AudioEngine
from ui_elements import Button
import threading

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

def render_fractal(visual_engine):
    while True:
        visual_engine.draw_fractal()
        visual_engine.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Audio-Visual Art Experience")

    # Initialize engines
    visual_engine = VisualEngine(screen)
    audio_engine = AudioEngine()

    # UI elements
    quit_button = Button(10, 10, 100, 40, "Quit")

    # Audio setup
    channel = pygame.mixer.find_channel()

    # Start a separate thread for fractal rendering
    render_thread = threading.Thread(target=render_fractal, args=(visual_engine,))
    render_thread.start()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_over(pygame.mouse.get_pos()):
                    running = False

        # Draw UI elements and update the display
        quit_button.draw(visual_engine.screen)
        pygame.display.flip()

        # Generate tone based on zoom factor
        sound = audio_engine.generate_tone_with_envelope(visual_engine.zoom)
        if not channel.get_busy():
            channel.play(sound)

    pygame.quit()

if __name__ == "__main__":
    main()
