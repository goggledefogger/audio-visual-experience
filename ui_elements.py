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
