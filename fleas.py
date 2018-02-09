import pygame

WIDTH = 75 # width of individual square
HEIGHT = 75 # height of individual square

BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def column_to_pixel(col_num, width=WIDTH):
    return col_num * width + 10

def row_to_pixel(row_num, height=HEIGHT):
    return row_num * height + 10

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super(Square, self).__init__()
        self.row = row
        self.col = col
        self.color = color

        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = column_to_pixel(col)
        self.rect.y = row_to_pixel(row)

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
        left = (column_to_pixel(0), row_to_pixel(row))
        right = (column_to_pixel(num_cols), row_to_pixel(row))
        pygame.draw.line(screen, color, left, right)

    for col in range(num_cols + 1):
        top = (column_to_pixel(col), row_to_pixel(0))
        bottom = (column_to_pixel(col), row_to_pixel(num_rows))
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

new_game(10, 10)
