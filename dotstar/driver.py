# -*- coding: utf-8 -*-
from machine import SPI
import time


class LedStrip:
    """
    Driver for APA102C ledstripes (Adafruit Dotstars) on the Wipy
    Connect
    CLK <---> GP14 (yellow cable)
    DI  <---> GP16 (green cable)
    """

    def __init__(self, leds):
        """
        :param int leds: number of LEDs on strio
        """
        self.ledcount = leds
        self.buffersize = self.ledcount * 4
        self.buffer = bytearray(self.ledcount * 4)
        self.emptybuffer = bytearray(self.ledcount * 4)
        for i in range(0, self.buffersize, 4):
            self.emptybuffer[i] = 0xff
            self.emptybuffer[i + 1] = 0x0
            self.emptybuffer[i + 2] = 0x0
            self.emptybuffer[i + 3] = 0x0
        self.startframe = bytes([0x00, 0x00, 0x00, 0x00])
        self.endframe = bytes([0xff, 0xff, 0xff, 0xff])
        self.spi = SPI(
            0,
            mode=SPI.MASTER,
            baudrate=8000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB
        )
        self.clear()

    def clear(self):
        self.buffer = self.emptybuffer[:]

    def set(self, led, red=0, green=0, blue=0, bri=0x1f):
        """
        :param int led: Index of LED
        :param int red, green, blue: 0-255
        :param int bri: Brightness 0-31
        """
        if led > self.ledcount:
            led %= self.ledcount

        if led < 0:
            led += self.ledcount

        frameheader = (0x07 << 5) | bri

        offset = led * 4
        self.buffer[offset] = frameheader
        self.buffer[offset + 1] = blue
        self.buffer[offset + 2] = green
        self.buffer[offset + 3] = red

    def send(self):
        self.spi.write(self.startframe + self.buffer)

if __name__ == '__main__':
    """Demo"""
    import os
    Dotty = LedStrip(240)
    Dotty.send()
    bri = 1
    while True:
        r1 = ord(os.urandom(1))
        r2 = ord(os.urandom(1))
        r3 = ord(os.urandom(1))
        for i in range(0, Dotty.ledcount):
            Dotty.clear()
            Dotty.set(led=i, red=r1, green=r2, blue=r3)
            Dotty.set(led=Dotty.ledcount - 1 - i, red=r3, green=r2, blue= r1)
            Dotty.set(led=(Dotty.ledcount // 2) - (i // 2), red=r2, green=r1, blue=r3)
            Dotty.set(led=(Dotty.ledcount // 2) + (i // 2), red=r2, green=r1, blue=r3)
            Dotty.send()
            time.sleep_ms(20)
