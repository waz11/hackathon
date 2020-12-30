import threading
import socket
import time
from protocol import *
from random import randrange
from threading import Thread
import sys

group1_clients = []
group2_clients = []
connections = []
score_client = {
    "group_1": 0,
    "group_2": 0,
}
threads_start=[]
threads_end = []

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


def start_client_game(con,end_game,msg):
    con, add = con[0], con[1]
    con.send(msg.encode())
    while time.time() < end_game:
        if time.time()>end_game:
            return
        ms = con.recv(1024)
        add_score(add)
    

def end_client_game(con,msg):
    con = con[0]
    con.send(msg.encode())
    con.close()
    

def get_end_game_msg():
    global group1_clients, group2_clients, score_client
    mesg = 'Game over!\n'
    mesg += f'Group 1 typed in {score_client["group_1"]} characters. Group 2 typed in {score_client["group_2"]} characters.\n'
    if score_client["group_1"] < score_client["group_2"]:
        mesg += 'Group 2 wins!\n\n'
        mesg += 'Congratulations to the winners:\n'
        mesg += '==\n'
        for client in group2_clients:
            mesg += client[1] + '\n'
    elif score_client["group_1"] > score_client["group_2"]:
        mesg += 'Group 1 wins!\n\n'
        mesg += 'Congratulations to the winners:\n'
        mesg += '==\n'
        for client in group1_clients:
            mesg += client[1] + '\n'
    else:
        mesg += 'its a tie!\n'
    return mesg


def game_mode():
    global connections,threads_start,threads_end
    time_begin = time.time()
    time_end = time_begin +10
    print("Start Game")
    start_msg = get_start_msg()
    threads_start = [] 
    for con in connections:
        threads_start.append(Thread(target=start_client_game, args=[con,time_end,start_msg]))
    for t in threads_start:
        t.start()
    while time.time()<time_end:
        None
    print("Ending Game!")
    end_msg = get_end_game_msg()
    threads_end = [] 
    for con in connections:
       threads_end.append(Thread(target=end_client_game, args=[con,end_msg]))
    for t in threads_end:
        t.start()
    print('​Game over, sending out offer requests...​')
    main()

def close_threads():
    global threads_start,threads_end,score_client,group1_clients,group2_clients
    for t in threads_start:
        t.kill()
        t.join()
    for t in threads_end:
        t.kill()
        t.join()
    score_client['group_1']=0
    score_client['group_2']=0
    group1_clients = []
    group2_clients = []

def main():
    global time_start_game
    close_threads()
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
