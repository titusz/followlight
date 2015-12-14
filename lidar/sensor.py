# -*- coding: utf-8 -*-
import struct
import driver
import config
try:
    import usocket as socket
except ImportError:
    import socket


class LidarSensor:
    """
    Continuously read distance data from LIDAR and sends it to a 'hub' via UDP
    """

    def __init__(self, hub_ip=config.HUB_IP, hub_port=config.HUB_PORT):
        self.hub_ip = hub_ip
        self.hub_port = hub_port
        self.lidar = driver.Lidar()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def transmit_forever(self):
        last = 0
        while True:
            cm = self.lidar.distance()
            if last not in (cm - 1, cm, cm + 1):
                data = struct.pack('!H', cm)
                self.socket.sendto(data, (self.hub_ip, self.hub_port))
                last = cm


if __name__ == "__main__":
    sensor = LidarSensor()
    sensor.transmit_forever()
