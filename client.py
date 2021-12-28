import socket
import os

port = 5000
header = 64
frmt = 'utf-8'
disconnect_msg = b'quit'
SERVER = '10.0.0.3'
Address = (SERVER, port)
byte = {0: [b'5', b'small'], 1: [b'6', b'medium'], 2: [b'4', b'huge']}


def send_files(ind: int):
    f = None
    if ind == 0:
        f = open("small.txt", "br")
    elif ind == 1:
        f = open("medium.mp3", "br")
    elif ind == 2:
        f = open("huge.mp4", "br")
    length = byte[ind][0] + b' ' * (header - 1)
    client.send(length)
    client.send(byte[ind][1])
    length = str(os.fstat(f.fileno()).st_size).encode(frmt)
    length += b' ' * (header - len(length))
    client.send(length)
    chunk = f.read(1024)
    while chunk:
        client.send(chunk)
        chunk = f.read(1024)
    client.close()


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(Address)
    inp = input("Enter message\n")
    if inp == 'quit':
        client.close()
        break
    elif inp == 'small':
        send_files(0)
    elif inp == 'medium':
        send_files(1)
    elif inp == 'huge':
        send_files(2)
