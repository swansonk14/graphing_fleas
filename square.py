import pygame
from constants import COLORS, COLOR_MAP, get_width, get_height
from helpers import column_to_pixel, row_to_pixel

class Square(pygame.sprite.Sprite):
    """A Square represents a colored location that a flea can move to."""

    def __init__(self,
                 board,
                 row,
                 col,
                 num_colors,
                 init_color=0,
                 cycle_size=None,
                 color_map=None,
                 visited=False,
                 coordinates=False):
        """Initializes the Square.

        Arguments:
            board(Board): The Board the Square will be a part of.
            row(int): The number of the row where this Square is located.
            col(int): The number of the column where this Square is located.
            num_colors(int): The number of possible colors this Square can take on.
                Max is the number of colors in COLORS in constants.py.
            init_color(int): The initial color of this Square.
            cycle_size(int): The number of colors to cycle at the end of the list
                of colors. Must be less than or equal to num_colors.
                (None to cycle through all the colors.)
            color_map(dict): A map from each color to the next color in the sequence.
                If None, the default color_map will be initialized in
                the method initialize_color_map.
            visited(bool): True to add an X to indicate which squares have been visited.
            coordinates(bool): True to add coordinates to squares.
        """

        super(Square, self).__init__()

        self.board = board
        self.row = row
        self.col = col
        self.num_colors = num_colors
        self.color = init_color
        self.cycle_size = cycle_size
        self.visited = visited
        self.coordinates = coordinates
        self.origin = (self.board.flea_rows[0], self.board.flea_cols[0])

        # Initialize color map
        self.color_map = color_map if color_map is not None else self.initialize_color_map()

        # Initialize square image
        self.image = pygame.Surface((get_width(), get_height()))
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

        if self.coordinates:
            self.add_coordinates()

    def initialize_color_map(self):
        """Initializes a map from each color to the next color in the sequence.

        color_map maps each color i to color i+1.
        Additionally, it maps the last color (color n) to
        color (n - self.cycle_size). If self.cycle_size is None,
        then it maps from color n to color 1 (equivalent to
        self.cycle_size = n).

        Ex. n = 5, cycle size = None

        0 --> 1 --> 2 --> 3 --> 4 --> 0

        Ex. n = 5, cycle size = 4

        0 --> 1 --> 2 --> 3 --> 4 --> 1

        Returns:
            A dictionary mapping each color to the next color.
        """

        cycle_size = self.cycle_size if self.cycle_size is not None else self.num_colors

        color_map = {i: i+1 for i in range(self.num_colors - 1)}
        color_map[self.num_colors - 1] = self.num_colors - cycle_size

        return color_map

    def add_visited(self):
        """Adds an X in the square."""

        top_left = (self.rect.x, self.rect.y)
        top_right = (self.rect.x + get_width(), self.rect.y)
        bottom_left = (self.rect.x, self.rect.y + get_height())
        bottom_right = (self.rect.x + get_width(), self.rect.y + get_height())

        pygame.draw.line(self.image, COLOR_MAP['gray'], (0, 0), (get_width(), get_height()))
        pygame.draw.line(self.image, COLOR_MAP['gray'], (get_width(), 0), (0, get_height()))

    def add_coordinates(self):
        """Adds coordinates to the square."""

        if self.board.num_rows == 1:
            message = '{}'.format(self.col - self.origin[1])
        elif self.board.num_cols == 1:
            message = '{}'.format(self.row - self.origin[0])
        else:
            message = '({},{})'.format(self.row - self.origin[0], self.col - self.origin[1])

        font = pygame.font.Font(None, min(get_width(), get_height()) // 3)
        text = font.render(message, True, COLOR_MAP['black'], COLOR_MAP['white'])
        text_rect = text.get_rect(center=(get_width() // 2, get_height() // 2))
        self.image.blit(text, text_rect)

    def change_color(self):
        """Changes the color of the Square to the next color according to self.color_map.

        Additionally, adds an X in the square if self.visited is True.
        """

        self.color = self.color_map[self.color]
        self.image.fill(COLORS[self.color])

        if self.visited:
            self.add_visited()

        if self.coordinates:
            self.add_coordinates()

    def next_color(self):
        """Changes the color of the Square to the next color."""

        self.color = (self.color + 1) % self.num_colors
        self.image.fill(COLORS[self.color])

    def previous_color(self):
        """Changes the color of the Square to the previous color."""

        self.color = (self.color - 1) % self.num_colors
        self.image.fill(COLORS[self.color])
