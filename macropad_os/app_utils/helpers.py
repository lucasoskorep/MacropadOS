def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)


def rgb_from_int(rgb):
    blue = rgb & 255
    green = (rgb >> 8) & 255
    red = (rgb >> 16) & 255
    return red, green, blue