from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

"""def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print (msg)
        except OSError:  # Possibly client has left the chat.
            break"""

host = "127.0.0.1"
port = 33000

address = (host, port)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

#receive_thread = Thread(target = receive)

username = input("Username: ")
password = input("Password: ")

client_socket.send(bytes(username,"utf8"))
client_socket.send(bytes(password,"utf8"))
client_socket.close()