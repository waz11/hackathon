import struct
import ipaddress

MESSAGE_FORMAT = struct.Struct('!I')
IP = 'localhost'
PORT_GAME = 13117
SERVER_ADDRESS = ('localhost', 13117)
CLIENT1_ADDRESS = ('localhost', 1300)
CLIENT2_ADDRESS = ('localhost', 1301)


def protocol_write_message(sock, message):
    message_len = len(message)
    message = MESSAGE_FORMAT.pack(message_len) + message
    sock.sendall(message)


def protocol_read_message(sock):
    metadata = sock.recv(1024)
    message = metadata.decode()
    return message
