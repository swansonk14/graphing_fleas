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
        self.initialize_color_maps()
        self.color = self.colors[0]

        # Initialize square image
        self.image = pygame.Surface((get_width(), get_height()))
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def initialize_color_maps(self):
        """Initializes self.next_color_map and self.previous_color_map, which
        map from each color to the next or prevous color, respectively.

        If there are n colors total, self.next_color_map maps
        each color i to color i+1. Additionally, it maps the
        last color (color n) to color (n - self.cycle_size).

        Ex. n = 5, cycle size = 4

        1 --> 2 --> 3 --> 4 --> 5 --> 2

        self.previous_color_map maps each color i to color i-1.
        Additionally, it maps the first color (color 1) to
        itself. It ignores the cycle size.

        Ex. n = 5

        5 --> 4 --> 3 --> 2 --> 1 --> 1
        """

        first_color = self.colors[0]
        last_color = self.colors[-1]

        # Next color map
        self.next_color_map = {
            self.colors[i]: self.colors[i+1]
            for i in range(len(self.colors) - 1)
        }
        self.next_color_map[last_color] = self.colors[-self.cycle_size]

        # Previous color map
        self.previous_color_map = {
            self.colors[i]: self.colors[i-1]
            for i in range(1, len(self.colors))
        }
        self.previous_color_map[first_color] = first_color

    def next_color(self):
        """Changes the color of the Square to the next color.

        The next color is specified by the map self.next_color_map
        defined in the __init__ method. Also adds an X after
        changing the color if self.visited is True.
        """

        self.color = self.next_color_map[self.color]
        self.image.fill(COLORS[self.color])

        if self.visited:
            top_left = (self.rect.x, self.rect.y)
            top_right = (self.rect.x + get_width(), self.rect.y)
            bottom_left = (self.rect.x, self.rect.y + get_height())
            bottom_right = (self.rect.x + get_width(), self.rect.y + get_height())

            pygame.draw.line(self.image, COLORS['gray'], (0, 0), (get_width(), get_height()))
            pygame.draw.line(self.image, COLORS['gray'], (get_width(), 0), (0, get_height()))

    def previous_color(self):
        """Changes the color of the Square to the previous color.

        The previous color is specified by the map self.previous_color_map
        defined in the __init__ method.
        """

        self.color = self.previous_color_map[self.color]
        self.image.fill(COLORS[self.color])
