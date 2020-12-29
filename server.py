import threading
import socket
import time
from protocol import *
from random import randrange

group1_clients = []
group2_clients = []
connections = []
score_client = {
    "group_1": 0,
    "group_2": 0,
}


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
    global all_clients, group2_clients, group1_clients, connections
    print("start wait for client")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 1337))
        s.listen()
        conn, addr = s.accept()
        connections.append((conn, addr))
        print(f'New client: {addr}')
        team_name = protocol_read_message(conn)
        print("received message from client:", team_name)
        rnd = randrange(2)
        if rnd % 2 == 0:
            group1_clients.append((addr, team_name))
        else:
            group2_clients.append((addr, team_name))


def get_start_msg():
    global all_clients, group2_clients, group1_clients
    message = 'Welcome to keyboard Spamming Battle Royal.\n'
    message += 'Group 1:\n'
    message += '==\n'
    for client in group1_clients:
        message += client[1]
    message += '\n'
    message += 'Group 2:\n'
    message += '==\n'
    for client in group2_clients:
        message += client[1]
    message += '\nStart pressing keys on your keyboard as fast as you can!!\n'
    return message


def add_score(add):
    global score_client, group1_clients, group2_clients
    if add in [x[0] for x in group1_clients]:
        score_client['group_1'] += 1
    elif add in [x[0] for x in group2_clients]:
        score_client['group_2'] += 1
    else:
        print('address not playing...')


def game_mode():
    global connections
    print("start Game")
    start_msg = get_start_msg()
    for con in connections:
        con[0].send(start_msg.encode())

    con, add = connections[0][0], connections[0][1]
    while True:
        ms = con.recv(1024)
        print('adding score ', add)
        add_score(add)
        print(score_client)


def main():
    print("Server started, listening on IP address 172.1.0.4")
    now = time.time()
    future = now + 8
    send_offer(future)
    wait_for_client()
    while time.time() < future:
        None
    game_mode()


if __name__ == '__main__':
    main()
