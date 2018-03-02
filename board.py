import pygame
import random
from constants import COLOR_MAP
from helpers import row_column_to_pixels
from square import Square

class Board:
    """A Board contains, controls, and displays all Squares and Fleas in the simulation."""

    def __init__(self,
                 screen,
                 num_rows,
                 num_cols,
                 flea_class,
                 num_fleas,
                 flea_rows,
                 flea_cols,
                 init_directions,
                 square_colors,
                 image,
                 visited,
                 coordinates,
                 hide_grid):
        """Initializes the Board.

        Arguments:
            screen(Surface): A pygame Surface representing the screen display.
            num_rows(int): The number of rows in the Board.
            num_cols(int): The number of columns in the Board.
            flea_class(class): The class of the Fleas to create.
            num_fleas(int): The number of Fleas to create.
            flea_rows(list): The initial rows of the fleas.
                (None to start in the center vertically.
                 Unspecified fleas will be placed randomly.)
            flea_cols(list): The initial columns of the fleas.
                (None to start in the center horizontally.
                 Unspecified fleas will be placed randomly.)
            init_directions(list): The initial directions of the fleas.
                (Uspecified fleas will start facing up.)
            square_colors(list): Initial configuration of the colors of the squares.
                (list of list of ints representing square colors.)
                If None, all squares are initialized to color 0.
            image(str): Name of image file in images directory to use as the flea image.
            visited(bool): True to add an X to indicate which squares have been visited.
            coordinates(bool): True to add coordinates to squares.
            hide_grid(bool): True to hide the grid lines.
        """

        self.screen = screen
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.flea_class = flea_class
        self.num_fleas = num_fleas
        self.flea_rows, self.flea_cols = self.initialize_flea_locs(flea_rows, flea_cols)
        self.init_directions = self.initialize_flea_directions(init_directions)
        self.square_colors = self.initialize_square_colors(square_colors)
        self.image = image
        self.visited = visited
        self.coordinates = coordinates
        self.hide_grid = hide_grid

        self.squares = pygame.sprite.Group()
        self.board = []

        # Initialize squares on board
        for row in range(self.num_rows):
            row_squares = []

            for col in range(self.num_cols):
                square = Square(self,
                                row,
                                col,
                                self.flea_class.num_colors,
                                self.square_colors[row][col],
                                self.flea_class.cycle_size,
                                self.flea_class.color_map,
                                self.visited,
                                self.coordinates)
                self.squares.add(square)
                row_squares.append(square)

            self.board.append(row_squares)

        # Initialize fleas (first is centered, others are random)
        self.fleas = pygame.sprite.Group()
        for i in range(self.num_fleas):
            self.fleas.add(self.flea_class(self,
                                           self.flea_rows[i],
                                           self.flea_cols[i],
                                           self.init_directions[i],
                                           self.image))

    def initialize_flea_locs(self, flea_rows, flea_cols):
        """Determines the initial rows and columns of the fleas.

        Arguments:
            flea_rows(list): The initial rows of the fleas.
                (None to start in the center vertically.
                 Unspecified fleas will be placed randomly.)
            flea_cols(list): The initial columns of the fleas.
                (None to start in the center horizontally.
                 Unspecified fleas will be placed randomly.)

        Returns:
            A tuple of lists with the first list containing the
            initial rows of the fleas and the second list containing
            the initial columns of the fleas.
        """

        # Replace None with center
        flea_rows = [flea_row if flea_row is not None else self.num_rows // 2 for flea_row in flea_rows]
        flea_cols = [flea_col if flea_col is not None else self.num_cols // 2 for flea_col in flea_cols]

        # Replace negative with positive
        flea_rows = [flea_row if flea_row >= 0 else self.num_rows + flea_row for flea_row in flea_rows]
        flea_cols = [flea_col if flea_col >= 0 else self.num_cols + flea_col for flea_col in flea_cols]

        # Fill in remaining fleas with random
        flea_rows += [random.randint(0, self.num_rows - 1)] * (self.num_fleas - len(flea_rows))
        flea_cols += [random.randint(0, self.num_cols - 1)] * (self.num_fleas - len(flea_cols))

        return flea_rows, flea_cols

    def initialize_flea_directions(self, init_directions):
        """Determines the initial directions of the fleas.

        Arguments:
            init_directions(list): The initial directions of the fleas.
                (Uspecified fleas will start facing up.)

        Returns:
            A list of strings containing the initial directions
            of the fleas.
        """

        init_directions += ['up'] * (self.num_fleas - len(init_directions))

        return init_directions

    def initialize_square_colors(self, square_colors):
        """Determine the initial square colors.

        Arguments:
            square_colors(list): Initial configuration of the colors of the squares.
                (list of list of ints representing square colors.)
                If None, all squares are initialized to color 0.

        Returns:
            A list of lists containing the initial colors of all
            squares on the board.
        """

        if square_colors is None:
            square_colors = [[0] * self.num_cols] * self.num_rows

        return square_colors

    def get_square(self, row, col):
        """Gets the Square in a given row and column.

        Arguments:
            row(int): The row number.
            col(int): The column number.

        Returns:
            The Square in the provided row and column.
        """

        return self.board[row][col]

    def rotate_fleas(self):
        """Rotates all Fleas."""

        for flea in self.fleas.sprites():
            flea.rotate()

    def change_square_colors(self):
        """Changes the color of the Squares under the Fleas."""

        for flea in self.fleas.sprites():
            flea.square.change_color()

    def move_fleas(self):
        """Moves all Fleas."""

        for flea in self.fleas.sprites():
            flea.move()

    def draw_grid(self):
        """Draws a grid of lines to visualize separate the Squares."""

        # Draw horizontal lines
        for row in range(self.num_rows + 1):
            left = row_column_to_pixels(row, 0)
            right = row_column_to_pixels(row, self.num_cols)
            pygame.draw.line(self.screen, COLOR_MAP['gray'], left, right)

        # Draw vertical lines
        for col in range(self.num_cols + 1):
            top = row_column_to_pixels(0, col)
            bottom = row_column_to_pixels(self.num_rows, col)
            pygame.draw.line(self.screen, COLOR_MAP['gray'], top, bottom)

    def draw(self):
        """Draws the Board including the Squares, grid, and Fleas."""

        self.squares.draw(self.screen)
        if not self.hide_grid:
            self.draw_grid()
        self.fleas.draw(self.screen)
        pygame.display.flip()
