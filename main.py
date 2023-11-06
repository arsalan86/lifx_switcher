import sys, argparse
from loguru import logger as log
from controller import controller as ctr

# import heartrate; heartrate.trace(browser=True)
DEBUG = True
DEBUG = False

def skip_on_debug(func):
    
    def _wrapper(*args, **kwargs):
        
        if not DEBUG:
            func(*args, **kwargs)
        
        else:
            pass
    
    return _wrapper

def set_verbosity(verbosity_flag):
    
    log.remove()

    if DEBUG:
        log.add(sys.stderr, level="DEBUG")
    
    elif verbosity_flag:
        log.add(sys.stderr, level="INFO")
    
    else:
        log.add(sys.stderr, level="SUCCESS", format="{message}")

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--devices", type=int)
    parser.add_argument("--hsbk")
    parser.add_argument("--rgb")
    parser.add_argument("-u", "--hue")
    parser.add_argument("-s", "--sat")
    parser.add_argument("-b", "--brightness")
    parser.add_argument("-k", "--temp")
    parser.add_argument("-v", "--verbose", action="store_true")
    
    return parser.parse_args()

def rgb_to_hsb(rgb_color):

    log.debug("rgb to hsb")

    import colorsys

    rgb_color["r"] = rgb_color["r"] / 65535.0
    rgb_color["g"] = rgb_color["g"] / 65535.0
    rgb_color["b"] = rgb_color["b"] / 65535.0

    h, s, b = colorsys.rgb_to_hsv(**rgb_color)

    h = h * 360
    s = s * 100
    b = b * 100
    k = 2500 # default

    return [h,s,b,k]

def get_color_parameters(args):

    if args.rgb is not None:
        color_values = args.rgb.split(":")
        color_rgb = {
            "r": int(color_values[0]),
            "g": int(color_values[1]),
            "b": int(color_values[2])
        }
        color_values = rgb_to_hsb(color_rgb)


    elif args.hsbk is not None:
        color_values =  args.hsbk.split(":")

    else:
        color_values = [args.hue, args.sat, args. brightness, args.temp]

    if all(value is None for value in color_values):
        return None

    color = {
        "h": color_values[0],
        "s": color_values[1],
        "b": color_values[2],
        "k": color_values[3],
    }
    
    return color

# @skip_on_debug
def switch_lights(number_of_devices, color):
    
    log.info("Scanning for devices...")
    lights = ctr(number_of_devices)

    if color is None:
        log.info("Toggling power...")
        return lights.toggle_power()

    log.info(f"Setting color to {color}")

    return lights.set_color(color)

def main():

    args = parse_arguments()

    set_verbosity(args.verbose)

    if switch_lights(args.devices, get_color_parameters(args)):
        log.success("Done!")

if __name__=="__main__":
    main()