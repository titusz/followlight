# -*- coding: utf-8 -*-
import config
import struct
import driver

try:
    import usocket as socket
except ImportError:
    import socket


class LedServer:
    """
    Receive and execute LedStrip commands.

    Each message is 6 x 2 bytes:
        message_type, led_number, red, green, blue, brightness

    Message Types:
        0: Clear LED Buffer
        1: Set LED with (r, g, b, brightness) values
        2: Send Buffer to LedStrip

    """

    def __init__(self, ip=config.UDP_IP, port=config.UDP_PORT, num_leds=240):

        # Init and clear LED Strip
        self.ledstrip = driver.LedStrip(num_leds)
        self.ledstrip.clear()
        self.ledstrip.send()

        # Init UDP-Socket listener
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))

    def run_forever(self):

        sock = self.socket
        led = self.ledstrip

        while True:
            data = sock.recv(12)
            msg = struct.unpack('!HHHHHH', data)
            if msg[0] == 0:
                led.clear()
            elif msg[0] == 1:
                led.set(msg[1], msg[2], msg[3], msg[4], msg[5])
            elif msg[0] == 2:
                led.send()


if __name__ == "__main__":
    server = LedServer()
    server.run_forever()
