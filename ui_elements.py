import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.font = pygame.font.SysFont(None, 36)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.text_surface, text_rect)
    # def draw(self, screen):
    #   pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    #   screen.blit(self.text_surface, (self.x + 10, self.y + 10))


    def is_clicked(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def is_hovered(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def is_over(self, pos):
        """Check if the given position is over the button."""
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

# You can add more UI elements here in the future.
