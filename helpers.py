from constants import MARGIN_TOP, MARGIN_SIDE, get_width, get_height

def row_to_pixel(row_num):
    """Converts a row number to a pixel number.

    Arguments:
        row_num(int): The number of the row.

    Returns:
        The pixel corresponding to the row.
    """

    return row_num * get_height() + MARGIN_TOP

def column_to_pixel(col_num):
    """Converts a column number to a pixel number.

    Arguments:
        col_num(int): The number of the column.

    Returns:
        The pixel corresponding to the column.
    """

    return col_num * get_width() + MARGIN_SIDE // 2

def row_column_to_pixels(row_num, col_num):
    """Converts a row number and a column number to tuple of pixel numbers.

    Arguments:
        row_num(int): The number of the row.
        col_num(int): The number of the column.

    Returns:
        A tuple with the pixels corresponding to the row and column.
    """

    return (column_to_pixel(col_num), row_to_pixel(row_num))
