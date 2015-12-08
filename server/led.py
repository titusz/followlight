# -*- coding: utf-8 -*-
import socket
import struct


class RemoteStrip:

    def __init__(self, target_ip="192.168.2.39", target_port=6000):
        self.ip = target_ip
        self.port = target_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def clear(self):
        data = struct.pack('!BBBBBB', 0, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))

    def set(self, led=0, r=254, g=254, b=254, bri=15):
        data = struct.pack('!BBBBBB', 1, led, r, g, b, bri)
        self.socket.sendto(data, (self.ip, self.port))

    def send(self):
        data = struct.pack('!BBBBBB', 2, 0, 0, 0, 0, 0)
        self.socket.sendto(data, (self.ip, self.port))


if __name__ == "__main__":
    ledstrip = RemoteStrip()
    ledstrip.clear()
    ledstrip.send()
    while True:
        for x in range(240):
            ledstrip.set(x)
            if x >= 1:
                ledstrip.set(x - 1, 0, 0, 0, 0)
            ledstrip.send()
