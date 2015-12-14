# -*- coding: utf-8 -*-
import socket
import struct
import time


class RemoteStrip:

    def __init__(self, target_ip="192.168.2.38", target_port=6000):
        self.ip = target_ip
        self.port = target_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def clear(self):
        data = struct.pack('!HHHHHH', 0, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.002)

    def set(self, led=0, r=254, g=254, b=254, bri=15):
        data = struct.pack('!HHHHHH', 1, led, r, g, b, bri)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.002)

    def send(self):
        data = struct.pack('!HHHHHH', 2, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))
        time.sleep(0.002)


if __name__ == "__main__":
    from random import randint
    ledstrip = RemoteStrip()
    ledstrip.clear()
    ledstrip.send()
    bris = range(0, 32)
    while True:
        r1 = randint(0, 255)
        r2 = randint(0, 255)
        r3 = randint(0, 255)
        for i in range(0, 240):
            ledstrip.clear()
            ledstrip.set(led=i, r=r1, g=r2, b=r3)
            ledstrip.set(led=240 - 1 - i, r=r3, g=r2, b=r1)
            ledstrip.set(led=(240 // 2) - (i // 2), r=r2, g=r1, b=r3)
            ledstrip.set(led=(240 // 2) + (i // 2), r=r2, g=r1, b=r3)
            ledstrip.send()
