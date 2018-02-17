import json

def process_config(args):
    """Loads a config file and updates the args.

    Arguments:
        args(object): The program arguments.
    """

    with open(args.config, 'r') as config_file:
        args.config = json.load(config_file)

    args.square_colors = args.config.get('square_colors', None)

    if args.square_colors is not None:
        args.num_rows = len(args.square_colors)
        args.num_cols = len(args.square_colors[0])
    else:
        args.num_rows = args.config.get('num_rows', args.num_rows)
        args.num_cols = args.config.get('num_cols', args.num_cols)

    for arg in vars(args):
        setattr(args, arg, args.config.get(arg, getattr(args, arg)))
