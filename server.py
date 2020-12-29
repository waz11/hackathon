import threading
import socket
import time
from protocol import *
from random import randrange
from threading import Thread

group1_clients = []
group2_clients = []
connections = []
score_client = {
    "group_1": 0,
    "group_2": 0,
}
global time_start_game


def send_offer():
    global time_start_game
    t = threading.Timer(1.0, send_offer)
    if time.time() > time_start_game:
        t.cancel()
        return
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print('sending msg')
        s.sendto(b'offer', ('<broadcast>', 1300))
    t.start()


def handle_client(conn, addr):
    global group2_clients, group1_clients, connections
    connections.append((conn, addr))
    print(f'New client: {addr}')
    team_name = protocol_read_message(conn)
    print("received message from client:", team_name)
    rnd = randrange(10)
    if rnd % 2 == 0:
        group1_clients.append((addr, team_name))
    else:
        group2_clients.append((addr, team_name))


def wait_for_client():
    global group2_clients, group1_clients, connections, time_start_game
    print("start wait for client")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(SERVER_ADDRESS)
        s.listen(2)
        s.settimeout(9)
        while time.time() < time_start_game:
            try:
                Thread(target=handle_client, args=(s.accept())).start()
            except socket.timeout:
                pass


def get_start_msg():
    global group2_clients, group1_clients
    message = 'Welcome to keyboard Spamming Battle Royal.\n'
    message += 'Group 1:\n'
    message += '==\n'
    for client in group1_clients:
        message += client[1] + '\n'
    message += '\n'
    message += 'Group 2:\n'
    message += '==\n'
    for client in group2_clients:
        message += client[1] + '\n'
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


def start_client_game(con):
    con, add = con[0], con[1]
    start_msg = get_start_msg()
    con.send(start_msg.encode())
    while True:
        ms = con.recv(1024)
        print('adding score ', add)
        add_score(add)
        print(score_client)


def game_mode():
    global connections
    print("start Game")
    for con in connections:
        Thread(target=start_client_game, args=[con]).start()


def main():
    global time_start_game
    print("Server started, listening on IP address 172.1.0.4")
    now = time.time()
    time_start_game = now + 10
    send_offer()
    wait_for_client()
    while time.time() < time_start_game:
        None
    game_mode()


if __name__ == '__main__':
    main()
