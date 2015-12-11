# -*- coding: utf-8 -*-
import socket
import struct
import config


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.HUB_IP, config.HUB_PORT))

while True:
    data, addr = sock.recvfrom(64)
    for value in struct.unpack('!H', data):
        print("\r%d" % value, end=" ")
