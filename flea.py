import pygame
from abc import ABCMeta, abstractmethod
from constants import DIRECTIONS, get_width, get_height

FLEA_CLASSES = {}

def RegisterFlea(flea_class):
    def decorator(cls):
        FLEA_CLASSES[flea_class] = cls
        return cls

    return decorator

def get_flea(flea_name):
    """Gets the Flea class from the FLEA_CLASSES.

    Arguments:
        flea_name(str): The name of the class of Flea to get.

    Returns:
        The class corresponding to the Flea name provided.
    """

    if flea_name not in FLEA_CLASSES:
        raise Exception(
            'Flea class "{}" not in FLEA_CLASSES. '.format(flea_name) +
            'Available Fleas are {}'.format(FLEA_CLASSES.keys()))

    flea_class = FLEA_CLASSES[flea_name]

    return flea_class


class Flea(pygame.sprite.Sprite, metaclass=ABCMeta):
    """A Flea represents a flea which can move on the Board and change the color of Squares.

    Flea is an abstract class. Subclasses must implement the
    rotate method, which decides how the Flea will rotate
    based on which color Square it is currently on.
    """

    def __init__(self, board, row, col, direction='up'):
        """Initializes the Flea.

        Arguments:
            board(Board): The Board the Flea will be on.
            row(int): The row number where the Flea will start.
            col(int): The column number where the Flea will start.
            direction(str): The initial direction of the Flea.
        """

        super(Flea, self).__init__()
        self.initialize_directions()

        self.board = board
        self.row = row
        self.col = col
        self.direction = direction

        self.square = board.get_square(self.row, self.col)
        self.rect = self.square.rect
        self.set_image()

    def initialize_directions(self):
        """Initializes the directions the Flea can point.

        Also initializes two maps:
        - self.left_direction maps each direction to the direction
        to the left (90 degrees counterclockwise).
        - self.right_direction maps each direction to the direction
        to the right (90 degrees clockwise).
        """

        self.directions = ['up', 'right', 'down', 'left']
        self.left_direction = {
            self.directions[i]: self.directions[(i-1) % len(self.directions)]
            for i in range(len(self.directions))
        }
        self.right_direction = {
            self.directions[i]: self.directions[(i+1) % len(self.directions)]
            for i in range(len(self.directions))
        }

    def rotate_left(self):
        """Rotates the Flea to the left (90 degrees counterclockwise)."""

        self.image = pygame.transform.rotate(self.image, 90)
        self.direction = self.left_direction[self.direction]

    def rotate_right(self):
        """Rotates the Flea to the right (90 degrees clockwise)."""

        self.image = pygame.transform.rotate(self.image, -90)
        self.direction = self.right_direction[self.direction]

    @abstractmethod
    def rotate(self):
        """Rotates the Flea based on the color of the Square the Flea is on."""

        pass

    def move(self):
        """Moves the Flea."""

        self.row = (self.row + DIRECTIONS[self.direction][0]) % self.board.num_rows
        self.col = (self.col + DIRECTIONS[self.direction][1]) % self.board.num_cols
        self.square = self.board.get_square(self.row, self.col)
        self.rect = self.square.rect

    def step(self):
        """Rotates and moves the Flea."""

        self.rotate()
        self.move()

    def set_image(self):
        """Sets the image of the Flea and orients it correctly."""

        self.image = pygame.image.load('flea.jpg')
        self.image = pygame.transform.scale(self.image, (get_width(), get_height()))

        # Rotate if necessary
        if self.direction == 'right':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'left':
            self.image = pygame.transform.rotate(self.image, 90)


# https://en.wikipedia.org/wiki/Langton%27s_ant
@RegisterFlea('langtons_flea')
class LangtonsFlea(Flea):
    def rotate(self):
        if self.square.color == 'white':
            self.rotate_right()
        else:
            self.rotate_left()

@RegisterFlea('multi_color_flea')
class MultiColorFlea(Flea):
    def rotate(self):
        if self.square.color == 'white':
            num_rotations = 1
        elif self.square.color == 'black':
            num_rotations = 2
        elif self.square.color == 'red':
            num_rotations = 3
        elif self.square.color == 'green':
            num_rotations = 4
        elif self.square.color == 'blue':
            num_rotations = 5

        for _ in range(num_rotations):
            self.rotate_right()
