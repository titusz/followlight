# -*- coding: utf-8 -*-
import time
from dotstar import DotStar

dt = DotStar(240)
dt.clear()
dt.send()


def fade(led=6):
    dt.clear()
    dt.set(led - 10, 184, 134, 11, 1)
    dt.set(led - 9, 184, 134, 11, 2)
    dt.set(led - 8, 184, 134, 11, 3)
    dt.set(led - 7, 184, 134, 11, 4)
    dt.set(led - 6, 184, 134, 11, 5)
    dt.set(led - 5, 184, 134, 11, 6)
    dt.set(led - 4, 184, 134, 11, 7)
    dt.set(led - 3, 184, 134, 11, 8)
    dt.set(led - 2, 184, 134, 11, 12)
    dt.set(led - 1, 184, 134, 11, 16)
    dt.set(led, 0, 0, 254, 31)

    dt.send()
    time.sleep_ms(20)

while True:
    for x in range(11, 240):
        fade(x)
