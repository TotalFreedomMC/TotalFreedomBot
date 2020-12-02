import time

from telnetlib import Telnet

class telnet:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def connect(self, *username):
        self.session = Telnet(self.ip, self.port)
        for x in username:
            self.username = username[0]

        if b'Username:' in self.session.read_until(b'Username:', timeout = 3):
            time.sleep(0.5)
            self.session.write(bytes(self.username, 'ascii') + b"\r\n")
        if b'Password:' in self.session.read_until(b'Password:', timeout = 3):
            time.sleep(0.5)
            self.session.write(bytes(self.password, 'ascii') + b"\r\n")
        else:
            raise ConnectionError('Failed to establish telnet connection.')
