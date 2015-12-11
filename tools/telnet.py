# -*- coding: utf-8 -*-
import time
import logging
import telnetlib

log = logging.getLogger(__name__)


class TelnetClient:

    def __init__(self, host, user, pwd, ttl=15):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.ttl = ttl
        self.tn = None

    def soft_reset(self):
        self.write('raise SystemExit')
        log.info('Soft reset executed')

    def hard_reset(self):
        self.write('import machine')
        self.write('machine.reset()')
        self.write('\x04')
        log.info('Machine reseted.')

    def open(self):
        self.tn = telnetlib.Telnet(self.host, 23, self.ttl)
        if b'Login as: ' in self.tn.read_until(b'Login as: ', self.ttl):
            log.info('Connection established')
            self.write(self.user)
            if b'Password:' in self.tn.read_until(b'Password:', self.ttl):
                time.sleep(0.2)
                self.write(self.pwd)
                sentinel = b'for more information.'
                if sentinel in self.tn.read_until(sentinel, self.ttl):
                    log.info('Login success.')
                    return self.tn
        raise ConnectionError('Connection failed :(')

    def write(self, s):
        self.tn.write(bytes(s, 'ascii') + b"\r\n")

    def close(self):
        if self.tn:
            self.tn.close()
            self.tn = None
        log.info('Connection closed')
