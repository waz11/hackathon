import socket
from protocol import *
import getch
import time
from KBHit import KBHit
from prints import *

socket_game = None


def create_socket(server_port):
    global socket_game
    if socket_game is None:
        socket_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_game.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_game.bind(CLIENT2_ADDRESS)
        socket_game.connect(('localhost', server_port))


def receive_offer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', 1300))
        msg, addr = s.recvfrom(PORT_GAME)

        msg_data = struct.unpack('Ibh', msg)
        cookie = msg_data[0]
        type = msg_data[1]

        if cookie == MAGIC_COOKIE or type == MSG_TYPE and msg_data[2]:
            print_client_msg(
                f'Received offer from {addr},attempting to connect...')
            s_port = msg_data[2]
            return s_port
        else:
            receive_offer()


def send_team_name(team):
    global socket_game
    socket_game.sendall(team.encode())


def send_press(*args):
    global socket_game
    socket_game.send(b'key')


def game_mode():
    global socket_game
    mes = protocol_read_message(socket_game)
    end_time = time.time() + 10
    print_game_mode(mes)
    kb = KBHit()
    while time.time() < end_time:
        time.sleep(0.5)
        if kb.kbhit():
            kb.set_normal_term()
            kb = KBHit()
            send_press()


def close_connections():
    global socket_game
    socket_game.close()
    socket_game = None


def end_game():
    mes = protocol_read_message(socket_game)
    print_end_game_mode(mes)
    close_connections()
    time.sleep(2)
    main()


def main():
    team_name = 'team 2'

    print_client_msg("Client started, listening for offer requests...")
    s_port = receive_offer()
    create_socket(s_port)
    send_team_name(team_name)
    game_mode()
    end_game()


if __name__ == '__main__':
    main()
