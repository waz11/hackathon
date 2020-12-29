import socket
from protocol import *
import getch

socket_game = None


def create_socket():
    global socket_game
    if socket_game is None:
        socket_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_game.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_game.bind(CLIENT2_ADDRESS)
        socket_game.connect(SERVER_ADDRESS)


def receive_offer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', 1300))
        msg, addr = s.recvfrom(PORT_GAME)
        if msg == b'offer':
            print(f'Received offer from {addr},attempting to connect...')


def send_team_name(team):
    global socket_game
    socket_game.sendall(team.encode())


def send_press(*args):
    global socket_game
    print(' sending')
    socket_game.send(b'key')


def game_mode():
    global socket_game

    mes = protocol_read_message(socket_game)
    print(mes)
    while True:
        try:
            k = getch.getch()
            send_press()
        except getch.getche():
            print("typing...")


def main():
    team_name = 'team 1'
    print("Client started, listening for offer requests...")
    receive_offer()
    create_socket()
    send_team_name(team_name)
    game_mode()


if __name__ == '__main__':
    main()
