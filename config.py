import json

def process_config(args):
    """Loads a config file and updates the args.

    Arguments:
        args(object): The program arguments.
    """

    # If no config, return
    if args.config is None:
        args.square_colors = None
        return

    # Open config
    with open(args.config, 'r') as config_file:
        args.config = json.load(config_file)

    # Load square colors
    args.square_colors = args.config.get('square_colors', None)

    # Determine number of rows and columns
    # if square colors are specified
    if args.square_colors is not None:
        args.num_rows = len(args.square_colors)
        args.num_cols = len(args.square_colors[0])

    # Load all other variables from config
    # using value in args as default
    for arg in vars(args):
        setattr(args, arg, args.config.get(arg, getattr(args, arg)))
