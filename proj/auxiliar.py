import math


def calculate_dimensions(x, y, z):
    """
    Calculate the dimensions (height and width) of a rectangle
    that can fit the sum of x, y, and z, with dimensions as close as possible.

    Parameters:
    x, y, z (int or float): The values to be summed up.

    Returns:
    tuple: (height, width) of the rectangle
    """
    # Calculate the total area needed
    total_area = x + y + z

    # Start with the square root of the total area
    approx_side = math.ceil(math.sqrt(total_area))

    # Initialize height and width
    height = approx_side - 1
    width = approx_side - 1

    # Adjust dimensions to ensure area >= total_area
    while height * width < total_area:
        if height < width:  # Increase the smaller dimension
            height += 1
        else:
            width += 1

    return width, height
