import json
import socket
import threading
import time

from shared.ConstSock import ConstSock
from shared.Message import Login, Request, Response
from utils.auth.Authentication import Authentication
from utils.db.DBHandler import DBHandler
from utils.db.matches.DBMatchesHandler import DBMatchesHandler
from utils.db.details.DBDetailsHandler import DBDetailsHandler

Thread = threading.Thread
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

    try:
        while True:
            userInfo = connection.recv(1024).decode("utf8") #Listen for mode request from client
            userInfo = json.loads(userInfo)

            if userInfo["code"] == Request.LOGIN_MODE: #Client request login mode
                connection.send(bytes(Request.LOGIN_MODE, "utf8"))
            elif userInfo["code"] == Request.REGISTER_MODE:
                connection.send(bytes(Request.REGISTER_MODE, "utf8"))
            elif userInfo["code"] == Request.CLOSE_CONNECTION:
                connection.send(bytes(Response.CLOSE_CONNECTION, "utf8"))
                raise Exception("Client interrupted")

            if userInfo["code"] == Request.LOGIN_MODE: #Client request login mode
                userInfo = connection.recv(1024).decode("utf8")
                auth = Authentication.checkLogin(json.loads(userInfo))

                if auth["status"] == True:
                    if auth["role"] == "client":
                        connection.send(bytes(Login.SUCCESS, "utf8"))
                    elif auth["role"] == "admin":
                        connection.send(bytes(Login.ADMIN_ACCESS, "utf8"))
                    break
                else:
                    connection.send(bytes(Login.FAILED, "utf8"))
            elif userInfo["code"] == Request.REGISTER_MODE: #Client request register mode
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
            res = json.loads(res)
            print("Client send: ", res, " from ", address)

            if res["code"] == Request.CLOSE_CONNECTION:
                connection.send(bytes(json.dumps({ "code": Response.CLOSE_CONNECTION }), "utf8"))
                connection.close()
                userConnections.remove(connection)
                addresses.remove(address)
                n = n - 1
                break

            if res["code"] == Request.VIEW_ALL_MATCHES:
                response = DBMatchesHandler.getAllMatches()
                matches = []
                if response["status"] == 500:
                    matches = []
                elif response["status"] == 200:
                    matches = response["data"]
                connection.send(bytes(json.dumps({ "code": Response.VIEW_ALL_MATCHES, "data": matches }),"utf8"))

            if res["code"] == Request.VIEW_MATCH_BY_ID:
                idMatch = res["data"]
                response = DBMatchesHandler.getMatchById(idMatch)
                connection.send(bytes(json.dumps({ "code": Response.VIEW_MATCH_BY_ID, "data": response }), "utf8"))

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
