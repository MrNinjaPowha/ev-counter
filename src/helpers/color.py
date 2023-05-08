def rgb(red: int, blue: int, green: int):
    """Returns a hex string from the rgb value given."""
    for value in (red, green, blue):
        if not 0 <= value <= 255:
            raise ValueError('Each value has to be between 0 and 255!')

    return '#%02x%02x%02x' % (red, blue, green)
