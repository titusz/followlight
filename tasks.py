# -*- coding: utf-8 -*-
import os
import sys
from ftplib import FTP
from invoke import ctask as task
from pprint import pprint
from tools import telnet


LIDAR = 'lidar'
DOTSTAR = 'dotstar'


def init(ctx, taskname):
    if not hasattr(ctx, 'current'):
        print('First command must be target machine. (eg. $inv lidar reset')
        sys.exit()
    else:
        fill = (taskname, ctx.current.name, ctx.current.host)
        print("Running task '%s' against '%s' (%s)" % fill)


def update_netcfg(ctx):
    c = ctx.current
    folder = os.path.abspath(c.name)
    if c.name in (LIDAR, DOTSTAR):
        tpl = "# -*- coding: utf-8 -*-\nSSID = '%s'\nPWD = '%s'\n"
        with open(os.path.join(folder, 'netcfg.py'), 'w') as netcfg:
            netcfg.write(tpl % (ctx.wlan.ssid, ctx.wlan.pwd))


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
def server(ctx):
    """Apply command to Raspberry PI server"""
    ctx['current'] = ctx.server


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
    update_netcfg(ctx)
    c = ctx.current
    if c.name in (LIDAR, DOTSTAR):
        ftp = FTP(c.host, c.user, c.pwd)
        print('Connected to:', ftp.getwelcome())
        ftp.cwd('/flash')
        for f in os.listdir(os.path.join(os.getcwd(), c.name)):
            print('Uploading:', f)
            with open(f, 'rb') as upload_file:
                ftp.storbinary("STOR " + f, upload_file)


@task
def deploy(ctx):
    """Deploy code to machine (upload & reset)"""
    upload(ctx)
    reset(ctx)
