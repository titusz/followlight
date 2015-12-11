# -*- coding: utf-8 -*-
import os
import sys
from ftplib import FTP
from invoke import ctask as task
from pprint import pprint
from tools import telnet


LIDAR = 'lidar'
DOTSTAR = 'dotstar'
HUB = 'hub'


def init(ctx, taskname):
    if not hasattr(ctx, 'current'):
        print('First command must be target machine. (eg. $inv lidar reset')
        sys.exit()
    else:
        fill = (taskname, ctx.current.name, ctx.current.host)
        print("Running task '%s' against '%s' (%s)" % fill)


@task
def update_config(ctx):
    """Update machine configuration from invoke.yaml"""
    c = ctx.current
    folder = os.path.abspath(c.name)
    if c.name in (LIDAR, DOTSTAR, HUB):
        tpl = "# -*- coding: utf-8 -*-\nSSID = '%s'\nPWD = '%s'\n"
        with open(os.path.join(folder, 'config.py'), 'w') as cf:
            cf.write(tpl % (ctx.wlan.ssid, ctx.wlan.pwd))
            if c.name == DOTSTAR:
                cf.write("UDP_IP = '%s'\n" % c.host)
                cf.write('UPD_PORT = %s\n' % c.port)
            if c.name == LIDAR:
                cf.write("PIN_MONITOR = '%s'\n" % c.pin_monitor)
                cf.write("PIN_TRIGGER = '%s'\n" % c.pin_trigger)
                cf.write("HUB_IP = '%s'\n" % ctx.hub.ip)
                cf.write("HUB_PORT = %s\n" % ctx.hub.port)
            if c.name == HUB:
                cf.write("HUB_IP = '%s'\n" % c.ip)
                cf.write("HUB_PORT = %s\n" % c.port)


@task
def show_config(ctx):
    """Show current configuration"""
    pprint(dict(ctx))


@task
def lidar(ctx):
    """Apply command to WiPy with LIDAR Lite"""
    ctx['current'] = ctx.lidar


@task
def dotstar(ctx):
    """Apply Command to WiPy with DotStar"""
    ctx['current'] = ctx.dotstar


@task
def hub(ctx):
    """Apply command to Raspberry PI server"""
    ctx['current'] = ctx.hub


@task
def reset(ctx):
    """Reset machine"""
    init(ctx, 'reset')
    c = ctx.current
    tclient = telnet.TelnetClient(c.host, c.user, c.pwd)
    tclient.open()
    tclient.hard_reset()
    tclient.close()


@task
def upload(ctx):
    """Upload code to machine"""
    init(ctx, 'upload')
    update_config(ctx)
    c = ctx.current
    if c.name in (LIDAR, DOTSTAR):
        ftp = FTP(c.host, c.user, c.pwd)
        print('Connected to:', ftp.getwelcome())
        ftp.cwd('/flash')
        folder = os.path.abspath(os.path.join(os.getcwd(), c.name))
        for f in os.listdir(folder):
            if f.endswith('.py'):
                print('Uploading:', f)
                with open(os.path.join(folder, f), 'rb') as upload_file:
                    ftp.storbinary("STOR " + f, upload_file)


@task
def deploy(ctx):
    """Deploy code to machine (upload & reset)"""
    upload(ctx)
    reset(ctx)
