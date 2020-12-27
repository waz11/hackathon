import socket
from protocol import *

def udp_connection():
    print('Client started, listening for offer requests...')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(CLIENT1_ADDRESS)

    s.sendto(b'', SERVER_ADDRESS)

    msg, addr = s.recvfrom(1024)
    if msg == b'offer':
        print(f'Received offer from {addr},attempting to connect...')
    s.close()

def tcp_connection(team_name):
    s = socket.socket()
    s.connect(SERVER_ADDRESS)
    s.sendall(b'{team_name}+"\n"')
    data = s.recv(1024)
    print(f'Got from server: {data}')

    s.shutdown(socket.SHUT_RDWR)
    s.close()

def main():
    team_name = 'team1'
    udp_connection()
    tcp_connection(team_name)


if __name__ == '__main__':
    main()
