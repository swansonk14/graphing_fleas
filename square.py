import pygame
from constants import COLORS, get_width, get_height
from helpers import column_to_pixel, row_to_pixel

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, num_colors=2, color='white'):
        super(Square, self).__init__()
        self.row = row
        self.col = col
        self.num_colors = num_colors
        self.color = color

        # Initialize colors
        self.colors = ['white', 'black', 'red', 'green', 'blue'][:self.num_colors]
        self.next_color = {
            self.colors[i]: self.colors[(i+1) % len(self.colors)]
            for i in range(len(self.colors))
        }

        # Initialize square image
        self.image = pygame.Surface((get_width(), get_height()))
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def change_color(self):
        self.color = self.next_color[self.color]
        self.image.fill(COLORS[self.color])
