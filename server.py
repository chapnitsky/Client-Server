import socket
import threading
import time

header = 64
port = 5000
disconnect_msg = b'quit'
SERVER = '10.0.0.3'
Address = (SERVER, port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Address)
server.setblocking(True)


def handle(con, adr):
    print(f"[New Connection] {adr} connected.")
    connected = True
    f = None
    first = False
    length = None
    start_time = None
    while connected:
        length = con.recv(header)
        if not length:
            break
        if not start_time:
            start_time = time.time()
        ind = length.find(b' ')
        length = int(length[:ind])
        print(f"{length} Bytes")
        reading = True
        while reading and length != 0:
            if f:
                msg = con.recv(1024)
            else:
                msg = con.recv(length)
            if not msg:
                connected = False
                break
            if msg == b'small':
                f = open('small_of_' + adr[0] + '.txt', 'bw')
                first = True
            elif msg == b'medium':
                f = open('medium_of_' + adr[0] + '.mp3', 'bw')
                first = True
            elif msg == b'huge':
                f = open('huge_of_' + adr[0] + '.mp4', 'bw')
                first = True
            else:
                f.write(msg)

            if first:
                reading = False
                first = False
    con.close()
    if f:
        print("Message received in %s milliseconds\n" % int((time.time() - start_time)*1000))
        f.close()


def start():
    print(f"Listening on {SERVER}\n")
    server.listen()
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle, args=(con, adr))
        thread.start()
        print(f"[Active connections] {threading.activeCount() - 1}")


start()
