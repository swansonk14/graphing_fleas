import argparse
import pygame
from constants import COLORS, MARGIN_TOP, MARGIN_SIDE, set_width, set_height, get_width, get_height
from board import Board
from flea import get_flea, FLEA_CLASSES
from text import Text

def run_simulation(num_rows,
                   num_cols,
                   flea_class,
                   flea_row,
                   flea_col,
                   num_fleas,
                   visited,
                   display_frequency,
                   delay,
                   pause):
    """Runs a graphing fleas simulation.

    Arguments:
        num_rows(int): Number of rows in the board.
        num_cols(int): Number of columns in the board.
        flea_class(class): The class of the Fleas to create.
        flea_row(int): The initial row of the first flea.
            -1 to start in the center vertically.
        flea_col(int): The initial column of the first flea.
            -1 to start in the center horizontally.
        num_fleas(int): The number of Fleas to create.
        visited(bool): True to add an X to indicate which squares have been visited.
        display_frequency(int): How many steps between each update of the display.
            -1 to update manually upon pressing "d" key.
        delay(int): The number of milliseconds of delay between each step.
        pause(bool): True to start the game in a paused state.
    """

    pygame.init()

    window_size = (num_cols * get_width() + MARGIN_SIDE,
                   num_rows * get_height() + MARGIN_TOP + MARGIN_SIDE)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Graphing Fleas')

    board = Board(screen,
                  num_rows,
                  num_cols,
                  flea_class,
                  flea_row,
                  flea_col,
                  num_fleas,
                  visited)
    board.draw()

    text = Text(screen, board)
    text.update("Step 0{}".format(', PAUSED' if pause else ''))

    pygame.time.delay(500)

    quit = False
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
                    text.update("Step {}{}".format(step, ', PAUSED' if pause else ''))
                    board.draw()
        if quit:
            break

        # Take step
        if not pause:
            print("Step {}".format(step))

            # Update text displaying step number
            if display_frequency != -1 and step % display_frequency == 0:
                text.update("Step {}".format(step))

            # Rotate fleas
            board.rotate_fleas()

            if display_frequency != -1 and step % display_frequency == 0:
                board.draw()
                pygame.time.delay(delay)

            # Change square colors
            board.change_square_colors()

            # Move fleas
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
    parser.add_argument('--flea_name', type=str, default='langtons_flea', help='The name of the class of Flea to create. Options: {}'.format(', '.join(FLEA_CLASSES.keys())))
    parser.add_argument('--flea_row', type=int, default=-1, help='Initial row of first flea (-1 for center of board vertically)')
    parser.add_argument('--flea_col', type=int, default=-1, help='Initial column of first flea (-1 for center of board horizontally)')
    parser.add_argument('--num_fleas', type=int, default=1, help='Number of Fleas')
    parser.add_argument('--visited', action='store_true', default=False, help='Add an X to indicate which squares have been visited')
    parser.add_argument('--display_frequency', type=int, default=1, help='How often to update the display (-1 to update only on pressing "d" key)')
    parser.add_argument('--delay', type=int, default=0, help='Number of milliseconds between steps')
    parser.add_argument('--pause', action='store_true', default=False, help='Start the game in a paused state')
    args = parser.parse_args()

    set_width(args.width)
    set_height(args.height)

    flea_class = get_flea(args.flea_name)

    run_simulation(args.num_rows,
                   args.num_cols,
                   flea_class,
                   args.flea_row,
                   args.flea_col,
                   args.num_fleas,
                   args.visited,
                   args.display_frequency,
                   args.delay,
                   args.pause)
