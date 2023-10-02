import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=(150, 150, 150)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 25)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_over(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.x + (self.width / 2 - text_surface.get_width() / 2),
                                   self.y + (self.height / 2 - text_surface.get_height() / 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

class MuteButton(Button):
    def __init__(self, x, y, width, height, text, color, hover_color=(150, 150, 150), audio_engine=None):
        super().__init__(x, y, width, height, text, color, hover_color)
        self.audio_engine = audio_engine
        self.muted = False
        self.muted_color = (255, 0, 0)
        self.unmuted_color = (0, 255, 0)

    def toggle_mute(self):
        if self.audio_engine.muted:
            self.audio_engine.unmute()
            self.muted = False
        else:
            self.audio_engine.mute()
            self.muted = True

    def draw(self, screen):
        if self.muted:
            self.color = self.muted_color
        else:
            self.color = self.unmuted_color

        self.text = "Unmute" if self.muted else "Mute"
        super().draw(screen)

class VolumeSlider:
    def __init__(self, x, y, width, height, audio_engine, color=(200, 200, 200), knob_color=(50, 50, 50)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.audio_engine = audio_engine
        self.color = color
        self.knob_color = knob_color
        self.knob_width = 10
        self.knob_pos = self.x + (self.width - self.knob_width) * 0.2  # Start at 50% volume

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.knob_color, (self.knob_pos, self.y, self.knob_width, self.height))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(pygame.mouse.get_pos()):
            self.knob_pos = event.pos[0] - self.knob_width / 2
            self.update_volume()

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and self.is_over(pygame.mouse.get_pos()):
            self.knob_pos = event.pos[0] - self.knob_width / 2
            self.update_volume()

    def update_volume(self):
        volume_percentage = (self.knob_pos - self.x) / (self.width - self.knob_width)
        self.audio_engine.set_volume(volume_percentage)
