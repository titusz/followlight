# -*- coding: utf-8 -*-
import socket
import struct
import time
import config
import pytweening as tween
from inspect import getmembers


class RemoteStrip:

    def __init__(self, target_ip=config.DOTSTAR_IP, target_port=config.DOTSTAR_PORT):
        self.ip = target_ip
        self.port = target_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def clear(self):
        data = struct.pack('!HHHHHH', 0, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.001)

    def set(self, led=0, r=254, g=254, b=254, bri=15):
        data = struct.pack('!HHHHHH', 1, led % 240, r % 256, g % 256, b % 256, bri % 32)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.001)

    def send(self):
        data = struct.pack('!HHHHHH', 2, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.0001)


def forth_and_back():
    for x in range(240):
        yield x
    for y in reversed(range(240)):
        yield y


def easer():
    """Run all ease functions from pytweening on remote strip."""
    ledstrip = RemoteStrip()
    ledstrip.clear()
    ledstrip.send()
    last = 0
    funcs = [func[1] for func in getmembers(tween) if func[0].startswith('ease')]

    for func in funcs:
        print(func)
        for x in forth_and_back():
            ledstrip.set(last, 0, 0, 0, 0)
            prop = func(x / 240)
            led = abs(int(round(prop * 240)))
            ledstrip.set(led, 0, 255, 0, 31)
            ledstrip.send()
            last = led
            time.sleep(0.005)


if __name__ == "__main__":
    """Easer Demo

    Make sure LedServer is running on the Wipy.
    """
    easer()
