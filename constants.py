COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}

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
