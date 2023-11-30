import colorsys


def rgb_to_hsb(rgb_color):
    rgb_color["r"] = rgb_color["r"] / 65535.0
    rgb_color["g"] = rgb_color["g"] / 65535.0
    rgb_color["b"] = rgb_color["b"] / 65535.0

    h, s, b = colorsys.rgb_to_hsv(**rgb_color)

    h = h * 360
    s = s * 100
    b = b * 100
    k = 2500  # default

    return [h, s, b, k]


def hsb_to_rgb(hsbk):
    h, s, b, _ = hsbk

    h /= 360.0
    s /= 100.0
    b /= 100.0

    r, g, b = colorsys.hsv_to_rgb(h, s, b)

    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    return [r, g, b]
