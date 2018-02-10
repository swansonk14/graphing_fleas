# Graphing Fleas

Simulates the movement of fleas on a 2-dimensional grid. The fleas rotate depending on the color of the square they are currently on. The squares change color when fleas land on them.

Note: Requires Python 3.

## Running the simulation

To run the simulation, simply run:

```
python main.py
```

A number of optional arguments can be passed, including:

* `num_rows` - The number of rows in the grid.
* `num_cols` - The number of columns in the grid.
* `width` - The width (in pixels) of each square in the grid.
* `height` - The height (in pixels) of each square in the grid.
* `flea_name` - The name of the type of flea to simulate. Different fleas follow different rules.
* `num_fleas` - The number of fleas to simulate.
* `num_colors` - The number of colors each square can take on.
* `delay` - The number of milliseconds of delay between each step of the simulation.

Example:

```
python main.py --num_rows 75 --num_cols 150 --width 20 --height 20 --flea_name langtons_flea --num_fleas 20 --num_colors 5 --delay 0
```

## Authors
Kyle Swanson, Magdalen Dobson, Thomas Sturm
