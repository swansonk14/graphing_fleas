import pygame
from constants import COLORS, ORDERED_COLORS, get_width, get_height
from helpers import column_to_pixel, row_to_pixel

class Square(pygame.sprite.Sprite):
    """A Square represents a colored location that a flea can move to."""

    def __init__(self,
                 row,
                 col,
                 num_colors,
                 cycle_size=None,
                 color_map=None,
                 visited=False):
        """Initializes the Square.

        Arguments:
            row(int): The number of the row where this Square is located.
            col(int): The number of the column where this Square is located.
            num_colors(int): The number of possible colors this Square can take on.
                Max is the number of colors in COLORS in constants.py.
            cycle_size(int): The number of colors to cycle at the end of the list
                of colors. Must be less than or equal to num_colors.
                (None to cycle through all the colors.)
            color_map(dict): A map from each color to the next color in the sequence.
                If None, the default color_map will be initialized in
                the method initialize_color_map.
            visited(bool): True to add an X to indicate which squares have been visited.
        """

        super(Square, self).__init__()

        self.row = row
        self.col = col
        self.num_colors = num_colors
        self.cycle_size = cycle_size
        self.visited = visited

        # Initialize colors
        self.colors = ORDERED_COLORS[:self.num_colors]
        self.color = self.colors[0]
        self.color_map = color_map if color_map is not None else self.initialize_color_map()
        self.next_color_map = {
            self.colors[i]: self.colors[(i+1) % len(self.colors)]
            for i in range(len(self.colors))
        }
        self.previous_color_map = {
            self.colors[i]: self.colors[(i-1) % len(self.colors)]
            for i in range(len(self.colors))
        }

        # Initialize square image
        self.image = pygame.Surface((get_width(), get_height()))
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def initialize_color_map(self):
        """Initializes a map from each color to the next color in the sequence.

        color_map maps each color i to color i+1.
        Additionally, it maps the last color (color n) to
        color (n - self.cycle_size). If self.cycle_size is None,
        then it maps from color n to color 1 (equivalent to
        self.cycle_size = n).

        Ex. n = 5, cycle size = None

        1 --> 2 --> 3 --> 4 --> 5 --> 1

        Ex. n = 5, cycle size = 4

        1 --> 2 --> 3 --> 4 --> 5 --> 2

        Returns:
            A dictionary mapping each color to the next color.
        """

        last_color = self.colors[-1]
        cycle_size = self.cycle_size if self.cycle_size is not None else len(self.colors)

        color_map = {
            self.colors[i]: self.colors[i+1]
            for i in range(len(self.colors) - 1)
        }
        color_map[last_color] = self.colors[-cycle_size]

        return color_map

    def change_color(self):
        """Changes the color of the Square to the next color according to self.color_map.

        Additionally, adds an X in the square if self.visited is True.
        """

        self.color = self.color_map[self.color]
        self.image.fill(COLORS[self.color])

        if self.visited:
            top_left = (self.rect.x, self.rect.y)
            top_right = (self.rect.x + get_width(), self.rect.y)
            bottom_left = (self.rect.x, self.rect.y + get_height())
            bottom_right = (self.rect.x + get_width(), self.rect.y + get_height())

            pygame.draw.line(self.image, COLORS['gray'], (0, 0), (get_width(), get_height()))
            pygame.draw.line(self.image, COLORS['gray'], (get_width(), 0), (0, get_height()))

    def next_color(self):
        """Changes the color of the Square to the next color."""

        self.color = self.next_color_map[self.color]
        self.image.fill(COLORS[self.color])

    def previous_color(self):
        """Changes the color of the Square to the previous color."""

        self.color = self.previous_color_map[self.color]
        self.image.fill(COLORS[self.color])
