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
            'Flea class "{}" not in FLEA_CLASSES.'.format(flea_name) +
            'Available Fleas are {}'.format(FLEA_CLASSES.keys()))

    flea_class = FLEA_CLASSES[flea_name]

    return flea_class


class Flea(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, board, row, col, direction='up'):
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
        # Initialize directions and direction changes
        self.directions = ['up', 'right', 'down', 'left']
        self.right_direction = {
            self.directions[i]: self.directions[(i+1) % len(self.directions)]
            for i in range(len(self.directions))
        }
        self.left_direction = {
            self.directions[i]: self.directions[(i-1) % len(self.directions)]
            for i in range(len(self.directions))
        }

    def rotate_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.direction = self.left_direction[self.direction]

    def rotate_right(self):
        self.image = pygame.transform.rotate(self.image, -90)
        self.direction = self.right_direction[self.direction]

    @abstractmethod
    def rotate(self):
        pass

    def move(self):
        self.row = (self.row + DIRECTIONS[self.direction][0]) % self.board.num_rows
        self.col = (self.col + DIRECTIONS[self.direction][1]) % self.board.num_cols
        self.square = self.board.get_square(self.row, self.col)
        self.rect = self.square.rect

    def step(self):
        self.rotate()
        self.move()

    def set_image(self):
        self.image = pygame.image.load('flea.jpg')
        self.image = pygame.transform.scale(self.image, (get_width(), get_height()))

        # Rotate if necessary
        if self.direction == 'right':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'left':
            self.image = pygame.transform.rotate(self.image, 90)


@RegisterFlea("langtons_flea")
class LangtonsFlea(Flea):
    def rotate(self):
        if self.square.color == 'white':
            self.rotate_right()
        else:
            self.rotate_left()
