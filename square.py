import pygame
from constants import COLORS, ORDERED_COLORS, get_width, get_height
from helpers import column_to_pixel, row_to_pixel

class Square(pygame.sprite.Sprite):
    """A Square represents a colored location that a flea can move to."""

    def __init__(self, row, col, num_colors, cycle_size=None, visited=False):
        """Initializes the Square.

        Arguments:
            row(int): The number of the row where this Square is located.
            col(int): The number of the column where this Square is located.
            num_colors(int): The number of possible colors this Square can take on.
                Max is the number of colors in COLORS in constants.py.
            cycle_size(int): The number of colors to cycle at the end of the list
                of colors. Must be less than or equal to num_colors.
                (None to cycle through all the colors.)
            visited(bool): True to add an X to indicate which squares have been visited.
        """

        super(Square, self).__init__()

        self.row = row
        self.col = col
        self.num_colors = num_colors
        self.cycle_size = cycle_size if cycle_size is not None else num_colors
        self.visited = visited

        # Initialize colors
        self.colors = ORDERED_COLORS[:self.num_colors]
        self.initialize_next_color_map()
        self.color = self.colors[0]

        # Initialize square image
        self.image = pygame.Surface((get_width(), get_height()))
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def initialize_next_color_map(self):
        """Initializes self.next_color which maps from the
        current color to the next color."""

        self.next_color = {
            self.colors[i]: self.colors[i+1]
            for i in range(len(self.colors) - 1)
        }
        last_color = self.colors[-1]
        self.next_color[last_color] = self.colors[-self.cycle_size]

    def change_color(self):
        """Changes the color of the Square.

        The next color is specified by the map self.next_color
        defined in the __init__ method.
        """

        self.color = self.next_color[self.color]
        self.image.fill(COLORS[self.color])

        if self.visited:
            top_left = (self.rect.x, self.rect.y)
            top_right = (self.rect.x + get_width(), self.rect.y)
            bottom_left = (self.rect.x, self.rect.y + get_height())
            bottom_right = (self.rect.x + get_width(), self.rect.y + get_height())

            pygame.draw.line(self.image, COLORS['gray'], (0, 0), (get_width(), get_height()))
            pygame.draw.line(self.image, COLORS['gray'], (get_width(), 0), (0, get_height()))
