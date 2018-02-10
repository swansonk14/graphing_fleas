import pygame
from constants import COLORS, MARGIN_TOP, MARGIN_SIDE, get_width

class Text:
    def __init__(self, screen, grid, font_type=None, font_size=50):
        self.screen = screen
        self.grid = grid
        self.font_type = font_type
        self.font_size = font_size

        self.screen_width = self.grid.num_cols * get_width() + MARGIN_SIDE
        self.font = pygame.font.Font(self.font_type, self.font_size)

        self.top_area = pygame.Surface((self.screen_width, MARGIN_TOP))
        self.top_area.fill(COLORS['black'])

    def clear(self):
        self.screen.blit(self.top_area, self.top_area.get_rect())
        pygame.display.flip()

    def update(self, message):
        self.clear()
        text = self.font.render(message, True, COLORS['white'], COLORS['black'])
        text_rect = text.get_rect(center=(self.screen_width // 2, MARGIN_TOP // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
