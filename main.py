import argparse
import pygame
from constants import COLORS, MARGIN_TOP, MARGIN_SIDE, set_width, set_height, get_width, get_height
from board import Board
from flea import get_flea, FLEA_CLASSES
from text import Text

def format_step(step, threshold=10000):
    """Formats step to be in scientific notation once it exceeds the threshold.

    Arguments:
        step(int): Step number.
        threshold(int): The step number above which to use scientific notation.

    Returns:
        A string with step either as an int or in scientific notation.
    """

    if step >= threshold:
        return '{:.2e}'.format(step)
    
    return str(step)

def run_simulation(num_rows,
                   num_cols,
                   flea_class,
                   num_fleas,
                   flea_rows,
                   flea_cols,
                   visited,
                   display_frequency,
                   print_frequency,
                   delay,
                   pause):
    """Runs a graphing fleas simulation.

    Arguments:
        num_rows(int): Number of rows in the board.
        num_cols(int): Number of columns in the board.
        flea_class(class): The class of the Fleas to create.
        num_fleas(int): The number of Fleas to create.
        flea_rows(int): The initial rows of the fleas.
            (-1 to start in the center vertically.
             Unspecified fleas will be placed randomly.)
        flea_cols(int): The initial columns of the fleas.
            (-1 to start in the center horizontally.
             Unspecified fleas will be placed randomly.)
        visited(bool): True to add an X to indicate which squares have been visited.
        display_frequency(int): How many steps between each update of the display.
            -1 to update manually upon pressing "d" key.
        print_frequency(int): How often to print the step to the terminal.
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
                  num_fleas,
                  flea_rows,
                  flea_cols,
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
                    text.update("Step {}{}".format(format_step(step), ', PAUSED' if pause else ''))
                elif event.key == pygame.K_d:
                    text.update("Step {}{}".format(format_step(step), ', PAUSED' if pause else ''))
                    board.draw()
        if quit:
            break

        # Take step
        if not pause:
            if step % print_frequency == 0:
                print("Step {}".format(format_step(step)))

            # Update text displaying step number
            if display_frequency != -1 and step % display_frequency == 0:
                text.update("Step {}".format(format_step(step)))

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
    parser.add_argument('--num_fleas', type=int, default=1, help='Number of Fleas')
    parser.add_argument('--flea_rows', type=int, nargs='+', default=[-1], help='Initial row of fleas (-1 for center of board vertically; unspecified fleas will be placed randomly)')
    parser.add_argument('--flea_cols', type=int, nargs='+', default=[-1], help='Initial column of fleas (-1 for center of board horizontally; unspecified fleas will be placed randomly)')
    parser.add_argument('--visited', action='store_true', default=False, help='Add an X to indicate which squares have been visited')
    parser.add_argument('--display_frequency', type=str, default='1', help='How often to update the display (-1 to update only on pressing "d" key; may be in scientific notation)')
    parser.add_argument('--print_frequency', type=str, default='1e5', help='How often to print the step to the terminal (may be in scientific notation)')
    parser.add_argument('--delay', type=int, default=0, help='Number of milliseconds between steps')
    parser.add_argument('--pause', action='store_true', default=False, help='Start the game in a paused state')
    args = parser.parse_args()

    set_width(args.width)
    set_height(args.height)

    flea_class = get_flea(args.flea_name)

    display_frequency = int(float(args.display_frequency))
    print_frequency = int(float(args.print_frequency))

    run_simulation(args.num_rows,
                   args.num_cols,
                   flea_class,
                   args.num_fleas,
                   args.flea_rows,
                   args.flea_cols,
                   args.visited,
                   display_frequency,
                   print_frequency,
                   args.delay,
                   args.pause)
