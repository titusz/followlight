# -*- coding: utf-8 -*-
import machine
import network
import config

wlan = network.WLAN(mode=network.WLAN.STA)

wlan.connect(config.SSID, auth=(network.WLAN.WPA2, config.PWD), timeout=5000)
while not wlan.isconnected():
    machine.idle()
