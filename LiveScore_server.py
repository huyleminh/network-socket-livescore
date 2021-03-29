from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

host = "127.0.0.1"
port = 33000

address = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

server.listen(1)

print("Waiting...")

connect, ip = server.accept()

try:
    print("Connected by ip: ", ip)
    while True:
        msg = server.recv(1024)
        
        print("Server receive: " + msg)
except KeyboardInterrupt:
    connect.close()
finally:
    connect.close()