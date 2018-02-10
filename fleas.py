import argparse
import pygame

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'grey': (100, 100, 100),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}
DIRECTIONS = {
    'up': (0, 1),
    'right': (1, 0),
    'down': (0, -1),
    'left': (-1, 0)
}

def column_to_pixel(col_num):
    return col_num * WIDTH + 10

def row_to_pixel(row_num):
    return row_num * HEIGHT + 10

def column_row_to_pixels(row_num, col_num):
    return (column_to_pixel(col_num), row_to_pixel(row_num))

class Flea(pygame.sprite.Sprite):
    directions = ['up', 'right', 'down', 'left']
    right_direction = {directions[i]: directions[(i+1) % len(directions)] for i in range(len(directions))}
    left_direction = {directions[i]: directions[(i-1) % len(directions)] for i in range(len(directions))}

    def __init__(self, board, row, col, direction='up'):
        super(Flea, self).__init__()
        self.board = board
        self.row = row
        self.col = col
        self.rect = board.get_square(self.row, self.col).rect
        self.direction = direction
        self.set_pic()

    def rotate_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.direction = self.left_direction[self.direction]

    def rotate_right(self):
        self.image = pygame.transform.rotate(self.image, -90)
        self.direction = self.right_direction[self.direction]

    def step(self):
        self.row = (self.row + self.direction[0]) % board.num_rows
        self.col = (self.col + self.direction[1]) % board.num_cols
        self.rect = board.get_square(self.row, self.col).rect

    def set_pic(self):
        self.image = pygame.image.load('flea.jpg')

        if self.direction == self.right:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == self.down:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == self.left:
            self.image = pygame.transform.rotate(self.image, 90)

class Square(pygame.sprite.Sprite):
    colors = ['white', 'black' 'red', 'green', 'blue']
    next_color = {colors[i]: colors[(i+1) % len(colors)] for i in range(len(colors))}

    def __init__(self, row, col, color):
        super(Square, self).__init__()
        self.row = row
        self.col = col
        self.color = color

        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def change_color(self):
        self.color = self.next_color[self.color]

class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.squares = pygame.sprite.Group()
        self.board = []

        # Initialize squares on board
        for row in range(self.num_rows):
            row_squares = []

            for col in range(self.num_cols):
                square = Square(row, col, WHITE)
                self.squares.add(square)
                row_squares.append(square)

            self.board.append(row_squares)

        # Initialize flea
        self.flea = pygame.sprite.Group(Flea(self, num_rows // 2, num_cols // 2))

    def get_square(self, row, col):
        return self.board[row][col]

    def draw_grid(self, screen, color=GREY):
        # Draw horizontal lines
        for row in range(self.num_rows + 1):
            left = column_row_to_pixels(row, 0)
            right = column_row_to_pixels(row, self.num_cols)
            pygame.draw.line(screen, color, left, right)

        # Draw vertical lines
        for col in range(self.num_cols + 1):
            top = column_row_to_pixels(0, col)
            bottom = column_row_to_pixels(self.num_rows, col)
            pygame.draw.line(screen, color, top, bottom)

def new_game(num_rows, num_cols):
    pygame.init()

    window_size = (num_cols * HEIGHT + 200,
                   num_rows * WIDTH + 20)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Graphing Fleas')

    board = Board(num_rows, num_cols)

    board.squares.draw(screen)
    board.draw_grid(screen)
    board.flea.draw(screen)
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
