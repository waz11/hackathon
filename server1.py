import threading
import socket
import time
from protocol import *
from random import randrange

all_clients = []
group1_clients = []
group2_clients = []
score_client = {}


def send_offer(end_time):
    t = threading.Timer(1.0, send_offer, [end_time])
    if time.time() > end_time:
        t.cancel()
        return
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print('sending msg')
        s.sendto(b'offer', ('127.0.0.1', 7331))
    t.start()


def wait_for_client():
    global all_clients, group2_clients, group1_clients
    print("start wait for client")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 1337))
        s.listen()
        conn, addr = s.accept()
        print(f'New client: {addr}')
        team_name = protocol_read_message(conn)
        print("received message from client:", team_name)
        all_clients.append(team_name)
        rnd = randrange(2)
        if rnd % 2 == 0:
            group1_clients.append(team_name)
        else:
            group2_clients.append(team_name)


def get_start_msg():
    global all_clients, group2_clients, group1_clients
    message = 'Welcome to keyboard Spamming Battle Royal.\n'
    message += 'Group 1:\n'
    message += '==\n'
    for client in group1_clients:
        message += client
    message += '\n'
    message += 'Group 2:\n'
    message += '==\n'
    for client in group2_clients:
        message += client
    message += '\nStart pressing keys on your keyboard as fast as you can!!\n'
    return message


def add_score(add):
    global score_client
    if add in score_client:
        score_client[add] += 1
        return
    score_client[add] = 0


def game_mode():
    print("start Game")
    start_msg = get_start_msg()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(CLIENT1_ADDRESS)
        s.sendall(start_msg.encode())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('',1337))
        while True:
            s.listen()
            _, add = s.accept()
            print('adding score ',add)
            add_score(add)
    print("done")


def main():
    global all_clients
    print("Server started, listening on IP address 172.1.0.4")
    now = time.time()
    future = now + 4
    send_offer(future)
    wait_for_client()
    while time.time() < future:
        None
    game_mode()


if __name__ == '__main__':
    main()
