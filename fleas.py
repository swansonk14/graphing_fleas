import argparse
import pygame

BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def column_to_pixel(col_num):
    return col_num * WIDTH + 10

def row_to_pixel(row_num):
    return row_num * HEIGHT + 10

def column_row_to_pixels(row_num, col_num):
    return (column_to_pixel(col_num), row_to_pixel(row_num))

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super(Square, self).__init__()
        self.row = row
        self.col = col
        self.color = color

        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.squares = pygame.sprite.Group()

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.squares.add(Square(row, col, WHITE))

def draw_grid(screen, num_rows, num_cols, color=GREY):
    for row in range(num_rows + 1):
        left = column_row_to_pixels(row, 0)
        right = column_row_to_pixels(row, num_cols)
        pygame.draw.line(screen, color, left, right)

    for col in range(num_cols + 1):
        top = column_row_to_pixels(0, col)
        bottom = column_row_to_pixels(num_rows, col)
        pygame.draw.line(screen, color, top, bottom)

def new_game(num_rows, num_cols):
    pygame.init()

    window_size = (num_cols * HEIGHT + 200,
                   num_rows * WIDTH + 20)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Graphing Fleas')

    board = Board(num_rows, num_cols)

    board.squares.draw(screen)
    draw_grid(screen, num_rows, num_cols)
    pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_rows', type=int, default=20, help='Number of rows')
    parser.add_argument('--num_cols', type=int, default=20, help='Number of columns')
    parser.add_argument('--width', type=int, default=100, help='Width of each square (in pixels)')
    parser.add_argument('--height', type=int, default=100, help='Height of each square (in pixels)')
    args = parser.parse_args()

    WIDTH = args.width
    HEIGHT = args.height

    new_game(args.num_rows, args.num_cols)
