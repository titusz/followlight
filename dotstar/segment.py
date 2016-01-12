# -*- coding: utf-8 -*-
import driver


class LedSegment:

    def __init__(self, segment_size=8, total_size=240):
        self.segment_size = segment_size
        self.total_size = total_size
        self.strip = driver.LedStrip(total_size)
        self.strip.clear()
        self.strip.send()

    def set(self, led, red, green, blue):
        for pos in range(self.segment_size):
            cled = led + pos
            self.strip.set(cled, red, green, blue)
        self.strip.send()
