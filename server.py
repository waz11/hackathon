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
    game_mode()


# wait_for_client()  # TODO: stop the func after 10 sec
#     game_mode()
# for client in clients:
#     if client != conn:
#         protocol_write_message(client, message)

# server.shutdown(socket.SHUT_RDWR)

all_clients = []
group1_clients = []
group2_clients = []


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
    print("starting game")
    message = "Welcome to Keyboard Spamming Battle Royale.\n"
    message += "Group 1:\n"
    message += "==\n"
    for client in group1_clients:
        message += client
    message += "Group 2:\n"
    message += "==\n"
    for client in group2_clients:
        message += client
    message += "Start pressing keys on your keyboard as fast as you can!!\n"

    send_socket = socket.socket()
    send_socket.connect(CLIENT1_ADDRESS)
    send_socket.sendall(message.encode())
    send_socket.close()

    recieve_socket = socket.socket()
    recieve_socket.bind(SERVER_ADDRESS)
    recieve_socket.listen()
    conn, addr = recieve_socket.accept()
    client_input = protocol_read_message(conn)
    print('get')

    recieve_socket.close()


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
