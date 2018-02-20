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
    433...334
    4xx...xx4
    422...224
    """

    square_colors = np.zeros((3, len(x) + 2), dtype=int)
    square_colors[:, 0] = 4
    square_colors[:, -1] = 4
    square_colors[0, 1:-1] = 3
    square_colors[1, 1:-1] = [int(digit) for digit in x]
    square_colors[2, 1:-1] = 2

    set_width(75)
    set_height(75)

    run_simulation(num_rows=square_colors.shape[0],
                   num_cols=square_colors.shape[1],
                   flea_class=BitFlipperFlea,
                   num_fleas=1,
                   flea_rows=[2],
                   flea_cols=[-2],
                   init_directions=['left'],
                   square_colors=square_colors.tolist(),
                   delay=100,
                   pause=True)

def add_one(x):
    pass

def twos_complement(x):
    pass

def add(x, y):
    pass

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
