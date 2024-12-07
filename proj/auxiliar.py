import math

def calculate_dimensions(x, y, z):
    """
    Calculate the dimensions (height and width) of a rectangle
    that can fit the sum of x, y, and z, favoring a rectangle over a square.

    Parameters:
    x, y, z (int or float): The values to be summed up.

    Returns:
    tuple: (width, height) of the rectangle
    """
    # Calculate the total area needed
    total_area = x + y + z

    # Start with an initial guess for width and height
    width = math.ceil(math.sqrt(total_area) * 2)  #Para fazer um retangulo
    height = math.ceil(total_area / width)

    # Adjust dimensions to ensure area >= total_area
    while width * height < total_area:
        width += 1
        height = math.ceil(total_area / width)

    return width, height
