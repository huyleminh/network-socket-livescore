import socket

class ConstSock:
    IP_ADDRESS = socket.AF_INET
    PROTOCOL = socket.SOCK_STREAM

    DEFAULT_PORT = 30000
    HOST_IP = "172.20.10.3" # Loop back

    MAX_CLIENTS = 2
