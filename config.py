def process_config(args):
    # Load initial square colors
    if args.config is not None:
        with open(args.config, 'r') as config_file:
            args.config = json.load(config_file)
            args.square_colors = args.config['square_colors']
            args.num_rows = len(args.square_colors)
            args.num_cols = len(args.square_colors[0])
            args.flea_name = args.config.get('flea_name', args.flea_name)
            args.num_fleas = args.config.get('num_fleas', args.num_fleas)
            args.flea_rows = args.config.get('flea_rows', args.flea_rows)
            args.flea_cols = args.config.get('flea_cols', args.flea_cols)
