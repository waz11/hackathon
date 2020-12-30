import struct
import ipaddress

MESSAGE_FORMAT = struct.Struct('!I')
IP = 'localhost'
PORT_GAME = 13117
SERVER_ADDRESS = ('localhost', 13117)
SERVER_PORT = PORT_GAME
CLIENT1_ADDRESS = ('localhost', 1300)
CLIENT2_ADDRESS = ('localhost', 1301)
CLIENT3_ADDRESS = ('localhost', 1302)
CLIENT4_ADDRESS = ('localhost', 1303)
CLIENT5_ADDRESS = ('localhost', 1304)

MAGIC_COOKIE = 0xfeedbeef
MSG_TYPE = 0x2

def protocol_write_message(sock, message):
    message_len = len(message)
    message = MESSAGE_FORMAT.pack(message_len) + message
    sock.sendall(message)


def protocol_read_message(sock):
    metadata = sock.recv(1024)
    message = metadata.decode()
    return message
