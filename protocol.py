import struct

MESSAGE_FORMAT = struct.Struct('!I')
SERVER_ADDRESS = ('127.0.0.1', 1337)
CLIENT1_ADDRESS = ('127.0.0.1', 7331)


def protocol_write_message(sock, message):
    message_len = len(message)
    message = MESSAGE_FORMAT.pack(message_len) + message
    sock.sendall(message)


def protocol_read_message(sock):
    # metadata = sock.recv(MESSAGE_FORMAT.size)
    # message_len = MESSAGE_FORMAT.unpack(metadata)[0]
    # return sock.recv(message_len)
    metadata = sock.recv(1024)
    message = metadata.decode()
    return message
