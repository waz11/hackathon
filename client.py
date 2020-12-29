import socket
from protocol import *
from pynput.keyboard import Key, Listener
import getch

socket_game = None


def create_socket():
    global socket_game
    if socket_game is None:
        socket_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_game.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_game.bind(CLIENT1_ADDRESS)
        socket_game.connect(SERVER_ADDRESS)


def receive_offer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(CLIENT1_ADDRESS)
        msg, addr = s.recvfrom(1337)
        if msg == b'offer':
            print(f'Received offer from {addr},attempting to connect...')


def send_team_name(team):
    global socket_game
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect(SERVER_ADDRESS)
    #     s.sendall(team.encode())
    socket_game.sendall(team.encode())


def send_press(*args):
    global socket_game
    print(' sending')
    socket_game.send(b'key')
    # return
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     s.bind(CLIENT1_ADDRESS)
    #     s.connect(SERVER_ADDRESS)
    #     s.send(b'')


def game_mode():
    global socket_game
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind(CLIENT1_ADDRESS)
    #     s.listen()
    #     conn, add = s.accept()
    #     mes = protocol_read_message(conn)
    #     print(mes)

    mes = protocol_read_message(socket_game)
    print(mes)
    while True:
        with Listener(on_release=send_press) as listener: listener.join()


def main():
    team_name = 'team 1'
    print("Client started, listening for offer requests...")
    receive_offer()
    create_socket()
    send_team_name(team_name)
    game_mode()


if __name__ == '__main__':
    main()
