import argparse

__all__ = ['bit_flip', 'add_one', 'twos_complement', 'add']

def bit_flip(x):
    pass

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

    # Parse inputs into ints using base
    args.input_1 = int(args.input_1, args.base)
    if args.input_2:
        args.input_2 = int(args.input_2, args.base)

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
