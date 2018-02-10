import pygame
from helpers import column_row_to_pixels
from flea import Flea
from square import Square

GREY = (100, 100, 100)

class Board:
    def __init__(self, screen, num_rows, num_cols, num_colors=2, square_color='white'):
        self.screen = screen
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_colors = num_colors
        self.square_color = square_color

        self.squares = pygame.sprite.Group()
        self.board = []

        # Initialize squares on board
        for row in range(self.num_rows):
            row_squares = []

            for col in range(self.num_cols):
                square = Square(row, col, self.num_colors, self.square_color)
                self.squares.add(square)
                row_squares.append(square)

            self.board.append(row_squares)

        # Initialize flea
        self.fleas = pygame.sprite.Group()
        self.fleas.add(Flea(self, num_rows // 2, num_cols // 2))

    def get_square(self, row, col):
        return self.board[row][col]

    def rotate_fleas(self):
        for flea in self.fleas.sprites():
            flea.rotate()

    def move_fleas(self):
        for flea in self.fleas.sprites():
            flea.move()

    def change_square_colors(self):
        for flea in self.fleas.sprites():
            flea.square.change_color()

    def draw_grid(self, screen):
        # Draw horizontal lines
        for row in range(self.num_rows + 1):
            left = column_row_to_pixels(row, 0)
            right = column_row_to_pixels(row, self.num_cols)
            pygame.draw.line(screen, GREY, left, right)

        # Draw vertical lines
        for col in range(self.num_cols + 1):
            top = column_row_to_pixels(0, col)
            bottom = column_row_to_pixels(self.num_rows, col)
            pygame.draw.line(screen, GREY, top, bottom)

    def draw(self):
        self.squares.draw(self.screen)
        self.draw_grid(self.screen)
        self.fleas.draw(self.screen)
        pygame.display.flip()
