# -*- coding: utf-8 -*-
"""Control an LED segment from orientation data of your android phone.

Parses data from the Android app Sensorstream IMU+GPS creates a moving segement
on the led strip based on orientation data. Activate "Orientation" and
"Include User-Checked Sensor Data in Stream" on the "Toogle Senors" Screen.
"""
import socket
import traceback
from collections import namedtuple
import led
import config


Message = namedtuple('Message', 'sid x y z')


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((config.HUB_IP, config.HUB_PORT))
led_strip = led.RemoteStrip()
led_strip.clear()
led_strip.send()
print('Orientation sensor running on %s:%s' % (config.HUB_IP, config.HUB_PORT))


def cycle():
    while True:
        for led in range(240):
            yield led
        for led in reversed(range(240)):
            yield led

c = cycle()

while True:

    try:
        message = s.recv(512)
        data = [round(float(d.strip())) % 255 for d in message.split(b',')]
        packet = Message(data[-4], data[-3], data[-2], data[-1])
        if packet.sid == 81:
            print(data[-4], data[-3], data[-2], data[-1])
            led_strip.clear()
            led_strip.set((data[-3] - 2) % 240, data[-3], data[-2], data[-1])
            led_strip.set((data[-3] - 1) % 240, data[-3], data[-2], data[-1])
            led_strip.set(data[-3] % 240, data[-3], data[-2], data[-1])
            led_strip.set((data[-3] + 1) % 240, data[-3], data[-2], data[-1])
            led_strip.set((data[-3] + 2) % 240, data[-3], data[-2], data[-1])
            led_strip.send()

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        traceback.print_exc()
