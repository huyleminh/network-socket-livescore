import socket
import threading
import json
import time

Thread = threading.Thread

from utils.auth.Authentication import Authentication
from shared.ConstSock import ConstSock
from shared.Message import Login

# Server socket
server = socket.socket(ConstSock.IP_ADDRESS, ConstSock.PROTOCOL)
server.bind((ConstSock.HOST_IP, ConstSock.DEFAULT_PORT))
server.listen(ConstSock.MAX_CLIENTS)

userConnections = []
addresses = []

def mainThreadServerSide():
    global server, addresses
    print("Waiting new connection")

    while True:
        try:
            connection, address = server.accept()
            print("Connected by ", address)
            addresses.append(address)

            Thread(target=clientThreadServerSide, args=(connection, address)).start()
        except KeyboardInterrupt:
            break

def clientThreadServerSide(connection, address):
    global userConnections
    userConnections.append(connection)

    # Todo: Force client to login first
    connection.send(bytes("Please login first: ", "utf8"))

    while True:
        userInfo = connection.recv(1024).decode("utf8")

        auth = Authentication.checkLogin(json.loads(userInfo))

        if auth == True:
            connection.send(bytes(Login.SUCCESS, "utf8"))
            break
        else:
            connection.send(bytes(Login.FAILED, "utf8"))

    # Done: Login Success
    while True:
        res = connection.recv(1024).decode("utf8")
        print("Client send: ", res, " from ", address)

        if res == "q":
            connection.send(bytes("qUiTqUiT", "utf8"))

            time.sleep(0.1)

            connection.close()
            userConnections.remove(connection)
            break

if __name__ == "__main__":
    print("Server is listening... ")
    serverThread = Thread(target=mainThreadServerSide)
    serverThread.start()
    serverThread.join()
    server.close() # Close after thread died