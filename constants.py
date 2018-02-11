COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'lime': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'silver': (192, 192, 192),
    'gray': (128, 128, 128),
    'maroon': (128, 0, 0),
    'olive': (128, 128, 0),
    'green': (0, 128, 0),
    'purple': (128, 0, 128),
    'teal': (0, 128, 128),
    'navy': (0, 0, 128)
}

ORDERED_COLORS = [
    'white',
    'black',
    'red',
    'lime',
    'blue',
    'yellow',
    'cyan',
    'magenta',
    'silver',
    'gray',
    'maroon',
    'olive',
    'green',
    'purple',
    'teal',
    'navy'
]

DIRECTIONS = {
    'up': (-1, 0),
    'right': (0, 1),
    'down': (1, 0),
    'left': (0, -1)
}

MARGIN_TOP = 50
MARGIN_SIDE = 20

width = 0
height = 0

def set_width(new_width):
	global width
	width = new_width

def set_height(new_height):
	global height
	height = new_height

def get_width():
	return width

def get_height():
	return height
