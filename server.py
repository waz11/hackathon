import socket
from protocol import *
import threading
from random import randrange
from threading import Thread

stop_thread = False


def send_offer(sock):
    global stop_thread
    t = threading.Timer(1.0, send_offer, [sock])
    t.start()
    print('sending msg')
    sock.sendto(b'offer', ('127.0.0.1', 7331))
    if stop_thread:
        t.cancel()


def finish_wait():
    global stop_thread
    stop_thread = True


def main():
    wait_for_client()
    print('done')
    game_mode()


# wait_for_client()  # TODO: stop the func after 10 sec
#     game_mode()
# for client in clients:
#     if client != conn:
#         protocol_write_message(client, message)

# server.shutdown(socket.SHUT_RDWR)


def wait_for_client():
    global stop_thread
    print('Server started,listening on IP address 172.1.0.4')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(SERVER_ADDRESS)
    threading.Timer(4.0, finish_wait).start()
    send_offer(s)

    server = socket.socket()
    server.bind(SERVER_ADDRESS)
    server.listen()

    all_clients = []
    group1_clients = []
    group2_clients = []

    conn, addr = server.accept()
    print(f'New client: {addr}')
    team_name = protocol_read_message(conn)
    print("received message from client:", team_name)
    all_clients.append(team_name)
    rnd = randrange(2)
    if rnd % 2 == 0:
        group1_clients.append(team_name)
    else:
        group2_clients.append(team_name)
    server.close()


def game_mode():
    print("Welcome to Keyboard Spamming Battle Royal")
    # to be continue


if __name__ == '__main__':
    main()

    # while True:
    #     msg, addr = s.recvfrom(1024)
    #     print(f'Got "{msg}" from {addr}')
    #     s.sendto(b'offer', addr)
    # print('server closed!')
    # s.close()
    #
    # server = socket.socket()
    # server.bind(SERVER_ADDRESS)
    # server.listen(5)
    #
    # clients = []
    #
    # while True:
    #     conn, addr = server.accept()
    #     print(f'New client: {addr}')
    #     clients.append(conn)
    #     message = protocol_read_message(conn)
    #     for client in clients:
    #         if client != conn:
    #             protocol_write_message(client, message)
    #
    # server.shutdown(socket.SHUT_RDWR)
    # server.close()
