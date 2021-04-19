import socket
import threading
import json
import time

Thread = threading.Thread

from utils.auth.Authentication import Authentication
from shared.ConstSock import ConstSock
from shared.Message import Login, Response, Request
from utils.db.DBHandler import DBHandler

# Server socket
server = socket.socket(ConstSock.IP_ADDRESS, ConstSock.PROTOCOL)
server.bind((ConstSock.HOST_IP, ConstSock.DEFAULT_PORT))
server.listen(ConstSock.MAX_CLIENTS)

userConnections = []
addresses = []
n = 0 #client counter

def mainThreadServerSide():
    global server, addresses
    print("Waiting new connection")
    global n
    while True:
        try:
            if n != ConstSock.MAX_CLIENTS:
                connection, address = server.accept()

                # Send success response to client
                print("Connected by ", address)
                connection.send(bytes(Response.SUCCESS_CONNECTION, "utf8"))

                addresses.append(address)
                n = n + 1

                Thread(target=clientThreadServerSide, args=(connection, address)).start()
            else: #handle more connections than max_connections case
                connection, address = server.accept()
                if n != ConstSock.MAX_CLIENTS:
                    # Send success response to client
                    print("Connected by ", address)
                    connection.send(bytes(Response.SUCCESS_CONNECTION, "utf8"))

                    addresses.append(address)
                    n = n + 1

                    Thread(target=clientThreadServerSide, args=(connection, address)).start()
                else:
                    print("Decline new connection due to too many connections")
                    connection.send(bytes(Response.EXCESS_CONNECTION, "utf8")) #send msg to force client close connection immediately
                    time.sleep(0.1)
                    connection.close()

        except KeyboardInterrupt:
            break

def clientThreadServerSide(connection, address):
    global userConnections
    userConnections.append(connection)
    global n
    # # Todo: Force client to login or register first
    # connection.send(bytes(Response.AUTHENTICATION_REQUEST, "utf8"))
    try:
        while True:
            userInfo = connection.recv(1024).decode("utf8") #Listen for mode request from client

            if userInfo == Request.LOGIN_MODE: #Client request login mode
                userInfo = connection.recv(1024).decode("utf8")
                auth = Authentication.checkLogin(json.loads(userInfo))

                if auth == True:
                    connection.send(bytes(Login.SUCCESS, "utf8"))
                    break
                else:
                    connection.send(bytes(Login.FAILED, "utf8"))
            elif userInfo == Request.REGISTER_MODE: #Client request register mode
                userInfo = connection.recv(1024).decode("utf8")
                auth = Authentication.checkRegister(json.loads(userInfo))

                if auth == True:
                    connection.send(bytes(Login.FAILED, "utf8"))
                else:
                    Authentication.registerNew(json.loads(userInfo))
                    connection.send(bytes(Login.SUCCESS, "utf8"))
                    break
            

        # Done: Login Success
        while True:
            res = connection.recv(1024).decode("utf8")
            print("Client send: ", res, " from ", address)

            if res == Request.CLOSE_CONNECTION:
                connection.send(bytes(Response.CLOSE_CONNECTION, "utf8"))

                time.sleep(0.1)

                connection.close()
                userConnections.remove(connection)
                addresses.remove(address)
                n = n - 1
                break

            if res == Request.VIEW_ALL_MATCHES:
                matches = DBHandler.readAllMatches()
                connection.send(bytes(json.dumps(matches),"utf8"))

    except: #Client suddenly drops connection
        print("Client ", address," error detected. Auto close connection.")
        connection.close()
        userConnections.remove(connection)
        addresses.remove(address)
        n = n - 1

if __name__ == "__main__":
    print("Server is listening... ")
    serverThread = Thread(target=mainThreadServerSide)
    serverThread.start()
    serverThread.join()
    server.close() # Close after thread died