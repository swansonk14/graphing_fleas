import pygame
import random
from constants import COLORS
from helpers import row_column_to_pixels
from square import Square

class Board:
    """A Board contains, controls, and displays all Squares and Fleas in the simulation."""

    def __init__(self,
                 screen,
                 num_rows,
                 num_cols,
                 flea_class,
                 flea_row,
                 flea_col,
                 num_fleas,
                 square_class,
                 num_colors):
        """Initializes the Board.

        Arguments:
            screen(Surface): A pygame Surface representing the screen display.
            num_rows(int): The number of rows in the Board.
            num_cols(int): The number of columns in the Board.
            flea_class(class): The class of the Fleas to create.
            flea_row(int): The initial row of the first flea.
                -1 to start in the center vertically.
            flea_col(int): The initial column of the first flea.
                -1 to start in the center horizontally.
            num_fleas(int): The number of Fleas to create.
            square_class(class): The class of the Squares to create.
            num_colors(int): The number of possible colors each Square can take on.
        """

        self.screen = screen
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.flea_class = flea_class
        self.flea_row = flea_row if flea_row != -1 else num_rows // 2
        self.flea_col = flea_col if flea_col != -1 else num_cols // 2
        self.num_fleas = num_fleas
        self.square_class = square_class
        self.num_colors = num_colors

        self.squares = pygame.sprite.Group()
        self.board = []

        # Initialize squares on board
        for row in range(self.num_rows):
            row_squares = []

            for col in range(self.num_cols):
                square = self.square_class(row, col, self.num_colors)
                self.squares.add(square)
                row_squares.append(square)

            self.board.append(row_squares)

        # Initialize fleas (first is centered, others are random)
        self.fleas = pygame.sprite.Group()
        self.fleas.add(self.flea_class(self, self.flea_row, self.flea_col))
        for _ in range(self.num_fleas - 1):
            self.fleas.add(self.flea_class(self,
                                           random.randint(0, num_rows - 1),
                                           random.randint(0, num_cols - 1)))

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
            pygame.draw.line(self.screen, COLORS['gray'], left, right)

        # Draw vertical lines
        for col in range(self.num_cols + 1):
            top = row_column_to_pixels(0, col)
            bottom = row_column_to_pixels(self.num_rows, col)
            pygame.draw.line(self.screen, COLORS['gray'], top, bottom)

    def draw(self):
        """Draws the Board including the Squares, grid, and Fleas."""

        self.squares.draw(self.screen)
        self.draw_grid()
        self.fleas.draw(self.screen)
        pygame.display.flip()
