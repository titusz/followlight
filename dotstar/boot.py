# -*- coding: utf-8 -*-
import machine
import network
import netcfg

wlan = network.WLAN(mode=network.WLAN.STA)

wlan.connect(netcfg.SSID, auth=(network.WLAN.WPA2, netcfg.PWD), timeout=5000)
while not wlan.isconnected():
    machine.idle()
