# -*- coding: utf-8 -*-
import socket
import struct
import config
import led

distance_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
distance_sock.bind((config.HUB_IP, config.HUB_PORT))

led_strip = led.RemoteStrip()

while True:
    dist_data = distance_sock.recv(2)
    package = struct.unpack('!H', dist_data)
    distance = package[0]
    print('Received distance:', distance, 'cm')
    if 180 < distance < 570:
        led = int((distance - 180) * 0.6)
        if not 0 < led < 240:
            continue
        led_strip.clear()
        if led - 4 >= 0:
            led_strip.set(led - 4, 255, 255, 20, 10)
        if led - 3 >= 0:
            led_strip.set(led - 3, 255, 255, 20, 20)
        if led - 2 >= 0:
            led_strip.set(led - 2, 255, 255, 40, 24)
        if led - 1 >= 0:
            led_strip.set(led - 1, 255, 255, 60, 28)

        led_strip.set(led, 255, 255, 80, 31)

        if led + 1 <= 240:
            led_strip.set(led + 1, 255, 255, 60, 28)
        if led + 2 <= 240:
            led_strip.set(led + 2, 255, 255, 40, 24)
        if led + 3 <= 240:
            led_strip.set(led + 3, 255, 255, 20, 20)
        if led + 4 <= 240:
            led_strip.set(led + 4, 255, 255, 20, 10)
        led_strip.send()
        print('Set LED:', led)
    else:
        led_strip.clear()
        led_strip.send()
