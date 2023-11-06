import sys, getopt
from loguru import logger as log
from lifxlan import LifxLAN, Group

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

        h = round((int(kwargs['h']) / 360) * 65535)
        s = round((int(kwargs['s']) / 100) * 65535)
        b = round((int(kwargs['b']) / 100) * 65535)
        k = kwargs['k']
        
        return (h,s,b,k)