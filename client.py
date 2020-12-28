import socket
from protocol import *


def looking_for_server():
    print('Client started, listening for offer requests...')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(CLIENT1_ADDRESS)

    msg, addr = s.recvfrom(1337)
    if msg == b'offer':
        print(f'Received offer from {addr},attempting to connect...')
    s.close()


def connecting_to_server(team_name):
    s = socket.socket()
    s.connect(SERVER_ADDRESS)
    mes = team_name + "\n"
    s.sendall(mes.encode())
    s.close()


def game_mode():
    s = socket.socket()
    s.bind(CLIENT1_ADDRESS)
    s.listen()

    conn, addr = s.accept()
    message = protocol_read_message(conn)
    print(message)

    while True:
        inp = input()
        s.send(inp.encode())


def main():
    team_name = 'team1'
    looking_for_server()
    connecting_to_server(team_name)
    game_mode()


if __name__ == '__main__':
    main()
