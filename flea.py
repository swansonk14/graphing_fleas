import pygame
from abc import ABCMeta, abstractmethod
from constants import DIRECTIONS, get_width, get_height

FLEA_CLASSES = {}

def RegisterFlea(flea_name):
    def decorator(flea_class):
        FLEA_CLASSES[flea_name] = flea_class
        return flea_class

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


class Flea(pygame.sprite.Sprite):
    """A Flea represents a flea which can move on the Board and change the color of Squares.

    Flea is an abstract class. Subclasses must define the
    num_colors property and must implement the rotate method,
    which decides how the Flea will rotate based on which color
    Square it is currently on. Fleas may optionally define the
    cycle_size and color_map properties.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def num_colors(self):
        pass

    cycle_size = None
    color_map = None

    @abstractmethod
    def rotate(self):
        pass

    def __init__(self, board, row, col, init_direction='up', image='flea.png'):
        """Initializes the Flea.

        Arguments:
            board(Board): The Board the Flea will be on.
            row(int): The row number where the Flea will start.
            col(int): The column number where the Flea will start.
            init_direction(str): The initial direction of the Flea.
            image(str): Name of image file in images directory to use as the flea image.
        """

        super(Flea, self).__init__()

        self.initialize_directions()

        self.board = board
        self.row = row
        self.col = col
        self.direction = init_direction
        self.image_name = image

        self.square = self.board.get_square(self.row, self.col)
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

    def rotate_180(self):
        """Rotates the Flea 180 degrees."""

        self.rotate_right()
        self.rotate_right()

    def stop(self):
        """Stops the Flea."""

        self.direction = 'stop'

    def move(self):
        """Moves the Flea."""

        self.row = (self.row + DIRECTIONS[self.direction][0]) % self.board.num_rows
        self.col = (self.col + DIRECTIONS[self.direction][1]) % self.board.num_cols
        self.square = self.board.get_square(self.row, self.col)
        self.rect = self.square.rect

    def set_image(self):
        """Sets the image of the Flea and orients it correctly."""

        self.image = pygame.image.load('images/{}'.format(self.image_name))
        self.image = pygame.transform.scale(self.image, (get_width(), get_height()))

        # Rotate if necessary
        if self.direction == 'right':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'left':
            self.image = pygame.transform.rotate(self.image, 90)


@RegisterFlea('langtons')
class LangtonsFlea(Flea):
    """Langton's ant in flea form (https://en.wikipedia.org/wiki/Langton%27s_ant).

    Color 0: right
    Color 1: left
    """

    num_colors = 2

    def rotate(self):
        if self.square.color == 0:
            self.rotate_right()
        else:
            self.rotate_left()

@RegisterFlea('triangle')
class TriangleFlea(Flea):
    """RRLLLRLLLRRR flea."""

    num_colors = 12

    right_turn_colors = [0, 1, 5, 9, 10, 11]

    def rotate(self):
        if self.square.color in self.right_turn_colors:
            self.rotate_right()
        else:
            self.rotate_left()

@RegisterFlea('1d_visit')
class OneDimensionalVisitorFlea(Flea):
    """A flea which visits all squares in one dimension.

    Color 0: 180 degrees
    Color 1: straight
    """

    num_colors = 2
    cycle_size = 1

    def __init__(self, *args, **kwargs):
        super(OneDimensionalVisitorFlea, self).__init__(*args, **kwargs)

        # Start facing right
        self.rotate_right()

    def rotate(self):
        if self.square.color == 0:
            self.rotate_right()
            self.rotate_right()

@RegisterFlea('2d_visit')
class TwoDimensionalVisitorFlea(Flea):
    """A flea which visits all squares in two dimensions.

    Color 0: right
    Color 1: left
    Color 2: straight
    """

    num_colors = 3
    cycle_size = 1

    def rotate(self):
        if self.square.color == 0:
            self.rotate_right()
        elif self.square.color == 1:
            self.rotate_left()

@RegisterFlea('bit_flipper')
class BitFlipperFlea(Flea):
    """Flips the bits of a binary numbers.

    Color 0: straight
    Color 1: straight
    Color 2: right
    Color 3: left
    Color 4: stop

    Example:

    The flea starts facing left (L) on a 2.

    4333333333
    4011000110
    422222222L

    -->

    L444444444
    4011000110
    4444444444

    The flea ends facing left (L) on a 4.
    """

    num_colors = 5
    color_map = {
        0: 1,
        1: 0,
        2: 4,
        3: 4,
        4: 4,
    }

    def rotate(self):
        if self.square.color == 2:
            self.rotate_right()
        elif self.square.color == 3:
            self.rotate_left()
        elif self.square.color == 4:
            self.stop()

@RegisterFlea('add_one')
class AddOneFlea(Flea):
    """Adds one to a binary number.

    Requires initial setup of the board.
    To add 1 to an n-digit binary number,
    write the number on the board and precede
    the number by a 0. The row above the number
    should be all 3s and the row below the number
    should be all 2s. Add a column of 4s preceding
    the number and the rows of 3s and 2s to stop the
    flea.

    Color 0: 180 degrees
    Color 1: straight
    Color 2: right
    Color 3: left
    Color 4: stop

    Example:

    Let's say the binary number we want to add
    one to is 100111011. Note in the following
    that we precede the number with a 0.

    The flea starts facing left (L) on a 2.

    43333333333
    40100111011
    4222222222L

    -->

    43333333344
    40100111100
    42222222D44

    The flea ends facing down (D) on a 4.
    """

    num_colors = 5
    color_map = {
        0: 1,
        1: 0,
        2: 4,
        3: 4,
        4: 4,
    }

    def rotate(self):
        if self.square.color == 0:
            self.rotate_180()
        elif self.square.color == 2:
            self.rotate_right()
        elif self.square.color == 3:
            self.rotate_left()
        elif self.square.color == 4:
            self.stop()

@RegisterFlea('twos_complement')
class TwosComplementFlea(Flea):
    """Performs two's complement on a binary number.

    Flips the bits and then adds one.

    Requires initial setup of the board.
    (See example below.)

    Color 0: straight
    Color 1: straight
    Color 2: 180 degrees
    Color 3: right
    Color 4: left
    Color 5: right
    Color 6: left
    Color 7: straight
    Color 8: stop

    Example:

    Let's say the binary number we want to compute
    the two's complement of is 100111010. Note in the
    following that we precede the number with a 1.

    The flea starts facing left (L) on a 3.

    577777777775
    544444444445
    811001110108
    6333333333L6
    677777777776

    --> (bit flip stage)

    577777777775
    544444444445
    822112221218
    6D5555555556
    677777777776

    The flea is now facing down (D) on a 3.

    --> (add one stage)

    577777777775
    544444444U85
    822112221128
    855555555588
    877777777778

    The flea ends facing up (U) on an 8.

    Note that in the end, 1s still represents
    1s but 2s now represent 0s.
    """

    num_colors = 9
    color_map = {
        0: 1,
        1: 2,
        2: 1,
        3: 5,
        4: 6,
        5: 8,
        6: 8,
        7: 7,
        8: 8
    }

    def rotate(self):
        if self.square.color == 2:
            self.rotate_180()
        elif self.square.color in [3, 5]:
            self.rotate_right()
        elif self.square.color in [4, 6]:
            self.rotate_left()
        elif self.square.color == 8:
            self.stop()

@RegisterFlea('adder')
class AdderFlea(Flea):
    """Adds two binary numbers in O(n^2) time.

    Digit colors
    Color 0: straight
    Color 1: 180

    Sum colors
    Color 2: 180
    Color 3: right
    Color 4: left

    Colors 2 = 0
    Colors 3 = 1
    Color 4 never stays

    Directional colors
    Color 5: right
    Color 6: right
    Color 7: straight
    Color 8: stop
    """

    num_colors = 9
    color_map = {
        0: 0,
        1: 0,
        2: 3,
        3: 4,
        4: 2,
        5: 7,
        6: 6,
        7: 7,
        8: 8
    }

    def rotate(self):
        color = self.square.color

        if color in [1, 2]:
            self.rotate_180()
        elif color in [3, 5, 6]:
            self.rotate_right()
        elif color == 4:
            self.rotate_left()
        elif color == 8:
            self.stop()

@RegisterFlea('adder_fast')
class AdderFastFlea(Flea):
    """Adds two binary numbers in O(n) time.

    Same color scheme as AdderFlea but
    now color 6 turns left instead of right.
    """

    num_colors = 9
    color_map = {
        0: 0,
        1: 0,
        2: 3,
        3: 4,
        4: 2,
        5: 7,
        6: 6,
        7: 7,
        8: 8
    }

    def rotate(self):
        color = self.square.color

        if color in [1, 2]:
            self.rotate_180()
        elif color in [3, 5]:
            self.rotate_right()
        elif color in [4, 6]:
            self.rotate_left()
        elif color == 8:
            self.stop()
