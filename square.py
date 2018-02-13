import pygame
from constants import COLORS, ORDERED_COLORS, get_width, get_height
from helpers import column_to_pixel, row_to_pixel

SQUARE_CLASSES = {}

def RegisterSquare(square_class):
    def decorator(cls):
        SQUARE_CLASSES[square_class] = cls
        return cls

    return decorator

def get_square(square_name):
    """Gets the Square class from the SQUARE_CLASSES.

    Arguments:
        square_name(str): The name of the class of Square to get.

    Returns:
        The class corresponding to the Square name provided.
    """

    if square_name not in SQUARE_CLASSES:
        raise Exception(
            'Square class "{}" not in SQUARE_CLASSES. '.format(square_name) +
            'Available Squares are {}'.format(SQUARE_CLASSES.keys()))

    square_class = SQUARE_CLASSES[square_name]

    return square_class


@RegisterSquare('square')
class Square(pygame.sprite.Sprite):
    """A Square represents a colored location that a flea can move to."""

    def __init__(self, row, col, num_colors):
        """Initializes the Square.

        Arguments:
            row(int): The number of the row where this Square is located.
            col(int): The number of the column where this Square is located.
            num_colors(int): The number of possible colors this Square can take on.
        """

        super(Square, self).__init__()

        self.row = row
        self.col = col
        self.num_colors = num_colors

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
            self.colors[i]: self.colors[(i+1) % len(self.colors)]
            for i in range(len(self.colors))
        }

    def change_color(self):
        """Changes the color of the Square.

        The next color is specified by the map self.next_color
        defined in the __init__ method.
        """

        self.color = self.next_color[self.color]
        self.image.fill(COLORS[self.color])

@RegisterSquare('visited_square')
class VisitedSquare(Square):
    """The VisitedSquare adds an indicator once a Flea has reached the square."""

    def change_color(self):
        super(VisitedSquare, self).change_color()

        top_left = (self.rect.x, self.rect.y)
        top_right = (self.rect.x + get_width(), self.rect.y)
        bottom_left = (self.rect.x, self.rect.y + get_height())
        bottom_right = (self.rect.x + get_width(), self.rect.y + get_height())

        pygame.draw.line(self.image, COLORS['gray'], (0, 0), (get_width(), get_height()))
        pygame.draw.line(self.image, COLORS['gray'], (get_width(), 0), (0, get_height()))

@RegisterSquare('end_color_square')
class EndColorSquare(Square):
    """The EndColorSquare cycles through the colors until it
    reaches the final color, which never changes."""

    def initialize_next_color_map(self):
        self.next_color = {
            self.colors[i]: self.colors[i+1]
            for i in range(len(self.colors) - 1)
        }
        last_color = self.colors[-1]
        self.next_color[last_color] = last_color
