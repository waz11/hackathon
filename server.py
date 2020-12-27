import socket
from protocol import *
import threading


def main():
    print('Server started,listening on IP address 172.1.0.4')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(SERVER_ADDRESS)
    while True:
        msg, addr = s.recvfrom(1024)
        print(f'Got "{msg}" from {addr}')
        s.sendto(b'offer', addr)
    print('server closed!')
    s.close()


    server = socket.socket()
    server.bind(SERVER_ADDRESS)
    server.listen(5)


    clients = []

    while True:
        conn, addr = server.accept()
        print(f'New client: {addr}')
        clients.append(conn)
        message = protocol_read_message(conn)
        for client in clients:
            if client != conn:
                protocol_write_message(client, message)

    server.shutdown(socket.SHUT_RDWR)
    server.close()


if __name__ == '__main__':
    main()
