import struct
import ipaddress

MESSAGE_FORMAT = struct.Struct('!I')
IP = 'localhost'
PORT_GAME = 13117
SERVER_ADDRESS = ('172.1.0.35', 13117)
CLIENT1_ADDRESS = ('localhost', 1300)
CLIENT2_ADDRESS = (ipaddress.ip_address("10.0.0.7"), 13117)


def protocol_write_message(sock, message):
    message_len = len(message)
    message = MESSAGE_FORMAT.pack(message_len) + message
    sock.sendall(message)


def protocol_read_message(sock):
    metadata = sock.recv(1024)
    message = metadata.decode()
    return message
