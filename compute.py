import argparse
import json

import numpy as np

from constants import set_width, set_height
from flea import BitFlipperFlea, AddOneFlea, TwosComplementFlea, AdderFlea
from main import run_simulation

__all__ = ['bit_flip', 'add_one', 'twos_complement', 'add']

def bit_flip(x):
    """Sets up a BitFlipperFlea to flip the bits of x.

    Square colors
    433...33
    4xx...xx
    422...22
    """

    num_rows = 3
    num_cols = len(x) + 1

    square_colors = np.zeros((num_rows, num_cols), dtype=int)
    square_colors[:, 0] = 4
    square_colors[0, 1:] = 3
    square_colors[1, 1:] = [int(digit) for digit in x]
    square_colors[2, 1:] = 2

    set_width(75)
    set_height(75)

    run_simulation(num_rows=num_rows,
                   num_cols=num_cols,
                   flea_class=BitFlipperFlea,
                   num_fleas=1,
                   flea_rows=[2],
                   flea_cols=[-1],
                   init_directions=['left'],
                   square_colors=square_colors.tolist(),
                   delay=100,
                   pause=True)

def add_one(x):
    """Sets up an AddOneFlea to add one to x.

    333...33
    0xx...xx
    222...22
    """

    num_rows = 3
    num_cols = len(x) + 1

    square_colors = np.zeros((num_rows, num_cols), dtype=int)
    square_colors[0] = 3
    square_colors[1, 1:] = [int(digit) for digit in x]
    square_colors[2] = 2

    set_width(75)
    set_height(75)

    run_simulation(num_rows=num_rows,
                   num_cols=num_cols,
                   flea_class=AddOneFlea,
                   num_fleas=1,
                   flea_rows=[2],
                   flea_cols=[-1],
                   init_directions=['left'],
                   square_colors=square_colors.tolist(),
                   delay=100,
                   pause=True)

def twos_complement(x):
    """Sets up a TwosComplementFlea to compute the twos complement of x.

    Flips the bits and then adds one.

    In the end, 3 is 0 and 1 is 1.

    5777...775
    5444...445
    80xx...xx8
    6333...336
    6777...776
    """

    num_rows = 5
    num_cols = len(x) + 3

    square_colors = np.zeros((num_rows, num_cols), dtype=int)
    square_colors[0, 0] = 5
    square_colors[0, 1:-1] = 7
    square_colors[0, -1] = 5
    square_colors[1, 0] = 5
    square_colors[1, 1:-1] = 4
    square_colors[1, -1] = 5
    square_colors[2, 0] = 8
    square_colors[2, 1] = 0
    square_colors[2, 2:-1] = [int(digit) for digit in x]
    square_colors[2, -1] = 8
    square_colors[3, 0] = 6
    square_colors[3, 1:-1] = 3
    square_colors[3, -1] = 6
    square_colors[4, 0] = 6
    square_colors[4, 1:-1] = 7
    square_colors[4, -1] = 6

    set_width(75)
    set_height(75)

    run_simulation(num_rows=num_rows,
                   num_cols=num_cols,
                   flea_class=TwosComplementFlea,
                   num_fleas=1,
                   flea_rows=[3],
                   flea_cols=[-2],
                   init_directions=['left'],
                   square_colors=square_colors.tolist(),
                   delay=100,
                   pause=True)

def add(x, y):
    """Sets up an AdderFlea to add x and y.

    In the end, 2 is 0 and 3 is 1.

    855...556
    8xx...xx7
    8yy...yy7
    555...556
    222...228
    """

    length = max(len(x), len(y))

    num_rows = 5
    num_cols = length + 2

    square_colors = np.zeros((num_rows, num_cols), dtype=int)
    square_colors[0, 0] = 8
    square_colors[0, 1:-1] = 5
    square_colors[0, -1] = 6
    square_colors[1, 0] = 8
    square_colors[1, 1:-1] = [0] * (length - len(x)) + [int(digit) for digit in x]
    square_colors[1, -1] = 7
    square_colors[2, 0] = 8
    square_colors[2, 1:-1] = [0] * (length - len(y)) + [int(digit) for digit in y]
    square_colors[2, -1] = 7
    square_colors[3, :-1] = 5
    square_colors[3, -1] = 6
    square_colors[4, :-1] = 2
    square_colors[4, -1] = 8

    set_width(75)
    set_height(75)

    run_simulation(num_rows=num_rows,
                   num_cols=num_cols,
                   flea_class=AdderFlea,
                   num_fleas=1,
                   flea_rows=[3],
                   flea_cols=[-2],
                   init_directions=['left'],
                   square_colors=square_colors.tolist(),
                   delay=100,
                   pause=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--compute_type', type=str, required=True, help='Type of compute to perform. Options: {}'.format(__all__))
    parser.add_argument('--base', type=int, default=2, help='Base in which inputs will be entered')
    parser.add_argument('--input_1', type=str, required=True, help='First input')
    parser.add_argument('--input_2', type=str, help='Second input')
    args = parser.parse_args()

    # Convert inputs to binary strings
    args.input_1 = '{:b}'.format(int(args.input_1, args.base))
    if args.input_2:
        args.input_2 = '{:b}'.format(int(args.input_2, args.base))

    # Select compute type to perform
    if args.compute_type == 'bit_flip':
        bit_flip(args.input_1)
    elif args.compute_type == 'add_one':
        add_one(args.input_1)
    elif args.compute_type == 'twos_complement':
        twos_complement(args.input_1)
    elif args.compute_type == 'add':
        add(args.input_1, args.input_2)
    else:
        print('Error: compute type must be one of {}'.format(__all__))
