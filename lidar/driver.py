# -*- coding: utf-8 -*-
import time
from machine import Pin
import config


class Lidar:
    """PWM based driver for Pulselight LIDAR-Lite v2"""

    def __init__(self, p_mon=config.PIN_MONITOR, p_trig=config.PIN_TRIGGER):
        self.p_trig = Pin(p_trig, mode=Pin.OUT)
        self.p_mon = Pin(p_mon, mode=Pin.IN, pull=Pin.PULL_UP)

    def distance(self, reads=1):
        scans = []
        for f in range(0, reads):
            self.p_trig.value(0)
            while not self.p_mon():
                pass
            start = time.ticks_us()
            while self.p_mon():
                pass
            pw = time.ticks_diff(start, time.ticks_us()) - 15
            cm = pw // 10
            self.p_trig.value(1)
            scans.append(cm)
        return sum(scans) // len(scans)


if __name__ == "__main__":
    l = Lidar()
    while True:
        print("\r%d" % l.distance(), end=" ")
