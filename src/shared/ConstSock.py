import socket

class ConstSock:
    IP_ADDRESS = socket.AF_INET
    PROTOCOL = socket.SOCK_STREAM

    DEFAULT_PORT = 3000
    HOST_IP = "127.0.0.1" # Loop back

    MAX_CLIENTS = 10
