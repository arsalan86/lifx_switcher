import getopt
import sys

from lifxlan import Group, LifxLAN
from loguru import logger as log

from utils import hsb_to_rgb


class controller:
    def __init__(self, number_of_devices: int):
        self.__lifx = LifxLAN(number_of_devices)
        self.devices = self.__lifx.get_devices()
        self.group = Group(self.devices)

    def toggle_power(self):
        """
        Default is to toggle power without changing color, temp etc
        If any lights are on, they are toggled off and their labels are recorded
        If all lights are off, then the power is toggled for recorded lights
        """

        if self.devices is None:
            log.error("No devices found")
            return None

        if sum([device.get_power() for device in self.devices]) > 0:
            log.info("Some devices are on")
            self.group.set_power(0)

        else:
            self.group.set_power(1, duration=100)

        return True

    def set_color(self, color):
        color = self.resolve_color(**color)
        self.group.set_color(color, duration=100)
        self.group.set_power(1, duration=100)

        return True

    def resolve_color(self, **kwargs):
        h = round((int(kwargs["h"]) / 360) * 65535)
        s = round((int(kwargs["s"]) / 100) * 65535)
        b = round((int(kwargs["b"]) / 100) * 65535)
        k = kwargs["k"]

        return (h, s, b, k)

    def get_light_status(self):
        """
        Get the current power state and color of each light in the group.
        If power is 0, add 'state': 'off' to the result. If power is not 0, add 'state': 'on'.
        Note: get_power() returns 0 for off and 65535 for on since its a 16 bit unsigned int.
        """

        if self.devices is None:
            log.error("No devices found")
            return None

        status = []

        for device in self.devices:
            color_hsb = device.get_color()
            color_rgb = hsb_to_rgb(color_hsb)

            power = device.get_power()
            state_info = "off" if power == 0 else "on"
            light_info = {
                "label": device.get_label(),
                "power": power,
                "state": state_info,
                "color (HSBK)": color_hsb,
                "color (RGB)": color_rgb,
            }

            status.append(light_info)

        return status
