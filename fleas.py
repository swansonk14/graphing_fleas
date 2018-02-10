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
    'up': (-1, 0),
    'right': (0, 1),
    'down': (1, 0),
    'left': (0, -1)
}

def column_to_pixel(col_num):
    return col_num * WIDTH + 10

def row_to_pixel(row_num):
    return row_num * HEIGHT + 10

def column_row_to_pixels(row_num, col_num):
    return (column_to_pixel(col_num), row_to_pixel(row_num))

class Flea(pygame.sprite.Sprite):
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

    def rotate(self):
        if self.square.color == 'white':
            self.rotate_right()
        else:
            self.rotate_left()

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
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        # Rotate if necessary
        if self.direction == 'right':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'left':
            self.image = pygame.transform.rotate(self.image, 90)

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color='white'):
        super(Square, self).__init__()
        self.initialize_colors()

        self.row = row
        self.col = col
        self.color = color

        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(COLORS[self.color])
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(self.col)
        self.rect.y = row_to_pixel(self.row)

    def initialize_colors(self):
        self.colors = ['white', 'black', 'red', 'green', 'blue']
        self.next_color = {
            self.colors[i]: self.colors[(i+1) % len(self.colors)]
            for i in range(len(self.colors))
        }

    def change_color(self):
        self.color = self.next_color[self.color]
        self.image.fill(COLORS[self.color])

class Board:
    def __init__(self, screen, num_rows, num_cols, square_color='white'):
        self.screen = screen
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.squares = pygame.sprite.Group()
        self.board = []

        # Initialize squares on board
        for row in range(self.num_rows):
            row_squares = []

            for col in range(self.num_cols):
                square = Square(row, col, square_color)
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

    def draw_grid(self, screen, color='grey'):
        # Draw horizontal lines
        for row in range(self.num_rows + 1):
            left = column_row_to_pixels(row, 0)
            right = column_row_to_pixels(row, self.num_cols)
            pygame.draw.line(screen, COLORS[color], left, right)

        # Draw vertical lines
        for col in range(self.num_cols + 1):
            top = column_row_to_pixels(0, col)
            bottom = column_row_to_pixels(self.num_rows, col)
            pygame.draw.line(screen, COLORS[color], top, bottom)

    def draw(self):
        self.squares.draw(self.screen)
        self.draw_grid(self.screen)
        self.fleas.draw(self.screen)
        pygame.display.flip()

def new_game(num_rows, num_cols, speed):
    pygame.init()

    window_size = (num_cols * HEIGHT + 200,
                   num_rows * WIDTH + 20)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Graphing Fleas')

    board = Board(screen, num_rows, num_cols)
    board.draw()
    pygame.time.delay(2000)

    quit = False
    pause = False
    while True:
        # Check for quit or pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
        if quit:
            break

        # Take step
        if not pause:
            board.rotate_fleas()
            board.draw()
            pygame.time.delay(speed)

            board.change_square_colors()

            board.move_fleas()
            board.draw()
            pygame.time.delay(speed)

    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_rows', type=int, default=20, help='Number of rows')
    parser.add_argument('--num_cols', type=int, default=20, help='Number of columns')
    parser.add_argument('--width', type=int, default=100, help='Width of each square (in pixels)')
    parser.add_argument('--height', type=int, default=100, help='Height of each square (in pixels)')
    parser.add_argument('--speed', type=int, default=250, help='Number of milliseconds between steps')
    args = parser.parse_args()

    WIDTH = args.width
    HEIGHT = args.height

    new_game(args.num_rows, args.num_cols, args.speed)
