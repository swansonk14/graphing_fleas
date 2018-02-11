import argparse
import pygame
from constants import COLORS, MARGIN_TOP, MARGIN_SIDE, set_width, set_height, get_width, get_height
from board import Board
from flea import get_flea
from square import Square
from text import Text

def run_simulation(num_rows, num_cols, num_colors, flea_class, num_fleas, display_frequency, delay):
    """Runs a graphing fleas simulation.

    Arguments:
        num_rows(int): Number of rows in the board.
        num_cols(int): Number of columns in the board.
        flea_class(class): The class of the Fleas to be created.
        num_fleas(int): The number of Fleas to create.
        num_colors(int): The number of colors each square can take on.
        display_frequency(int): How many steps between each update of the display.
            -1 to update manually upon pressing "d" key.
        delay(int): The number of milliseconds of delay between each step.
    """

    pygame.init()

    window_size = (num_cols * get_width() + MARGIN_SIDE,
                   num_rows * get_height() + MARGIN_TOP)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Graphing Fleas')

    board = Board(screen, num_rows, num_cols, flea_class, num_fleas, num_colors)
    board.draw()

    text = Text(screen, board)
    text.update("Step 0")

    pygame.time.delay(1000)

    quit = False
    pause = False
    step = 0
    while True:
        # Check for quit or pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    text.update("Step {}{}".format(step, ', PAUSED' if pause else ''))
                elif event.key == pygame.K_d:
                    board.draw()
        if quit:
            break

        # Take step
        if not pause:
            text.update("Step {}".format(step))

            board.rotate_fleas()
            if display_frequency != -1 and step % display_frequency == 0:
                board.draw()
                pygame.time.delay(delay)

            board.change_square_colors()

            board.move_fleas()
            
            if display_frequency != -1 and step % display_frequency == 0:
                board.draw()
                pygame.time.delay(delay)

            step += 1

    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_rows', type=int, default=20, help='Number of rows')
    parser.add_argument('--num_cols', type=int, default=20, help='Number of columns')
    parser.add_argument('--width', type=int, default=75, help='Width of each square (in pixels)')
    parser.add_argument('--height', type=int, default=75, help='Height of each square (in pixels)')
    parser.add_argument('--flea_name', type=str, default='langtons_flea', help='The name of the class of Flea to create')
    parser.add_argument('--num_fleas', type=int, default=1, help='Number of Fleas')
    parser.add_argument('--num_colors', type=int, default=2, help='Number of square colors (min = 1, max = {})'.format(len(COLORS)))
    parser.add_argument('--display_frequency', type=int, default=1, help='How often to update the display (-1 to update only on pressing "d" key)')
    parser.add_argument('--delay', type=int, default=0, help='Number of milliseconds between steps')
    args = parser.parse_args()

    set_width(args.width)
    set_height(args.height)

    flea_class = get_flea(args.flea_name)

    run_simulation(args.num_rows, args.num_cols, args.num_colors, flea_class, args.num_fleas, args.display_frequency, args.delay)
