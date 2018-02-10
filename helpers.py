import constants

def column_to_pixel(col_num):
    return col_num * constants.WIDTH + 10

def row_to_pixel(row_num):
    return row_num * constants.HEIGHT + 10

def column_row_to_pixels(row_num, col_num):
    return (column_to_pixel(col_num), row_to_pixel(row_num))
