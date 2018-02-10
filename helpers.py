from constants import MARGIN_TOP, MARGIN_SIDE, get_width, get_height

def column_to_pixel(col_num):
    return col_num * get_width() + MARGIN_SIDE // 2

def row_to_pixel(row_num):
    return row_num * get_height() + MARGIN_TOP

def column_row_to_pixels(row_num, col_num):
    return (column_to_pixel(col_num), row_to_pixel(row_num))
