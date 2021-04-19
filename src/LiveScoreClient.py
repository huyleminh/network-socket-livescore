import socket
import threading
import json
import time

from shared.Message import Login, Response, Request

IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

Thread = threading.Thread

HOST = "127.0.0.1"
PORT = 30000

# Client socket
client = socket.socket(IPV4, TCP)
client.connect((HOST, PORT))

login = False
connected = False
mode = 1 #Login mode(1) or Register mode(2)
#Please change mode in source code while waiting for UI

def receive():
    global login, connected
    try:
        # Receive response from server
        msg =  client.recv(1024).decode("utf8")

        if msg == Response.EXCESS_CONNECTION: #msg indicate that there are too many connection, force close
            print("Connection denied, queue is overflow. Please try again later.")
            client.close()
        elif msg == Response.SUCCESS_CONNECTION:
            connected = True
            print("Connect successfully.")

        # Done: connect sucessfully
        while connected == True:
            # ? Try to login
            while login == False:
                if mode == 1:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        print("Login successfully.")
                        login = True
                        break
                    elif msg == Login.FAILED:
                        print("Unable to login, please try again.")
                        login = False
                elif mode == 2:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        print("Register successfully.")
                        login = True
                        break
                    elif msg == Login.FAILED:
                        print("Account existed.")
                        login = False

            # Listen response from server
            msg = client.recv(1024).decode("utf8")
            if len(msg) > 0:
                if msg == Response.CLOSE_CONNECTION:
                    break
                print("Receive: " + msg)

        client.close()
    except:
        print("Server error detected. Press enter to close connection.")
        connected = False
        client.close()

def send():
    global login, connected, mode
    while connected == True:
        # ? Try to login
        while login == False:
            try:
                if mode == 1: #Login mode
                    client.send(bytes(Request.LOGIN_MODE, "utf8"))
                    print("Input Login Info")
                    username = input("Username: ")
                    password = input("Password: ")

                    userInfo = { "username": username, "password": password }
                    client.send(bytes(json.dumps(userInfo), "utf8"))
                    time.sleep(0.1)
                    
                if mode == 2: #Register mode
                    client.send(bytes(Request.REGISTER_MODE, "utf8"))
                    print("Input Register Info")
                    username = input("Username: ")
                    password = input("Password: ")

                    userInfo = { "username": username, "password": password, "role": "client"}
                    client.send(bytes(json.dumps(userInfo), "utf8"))
                    time.sleep(0.1)
            except:
                print("Login/Register error detected.")
                client.close()

        try:
            requestMsg = input("Enter 0 to view all matches\nEnter q to exit")
            #requestMsg = input("Request: ")
            if len(requestMsg) == 0:
                continue

            if connected == False:
                break

            if requestMsg == "0":
                client.send(bytes(Request.VIEW_ALL_MATCHES, "utf8"))
            #client.send(bytes(requestMsg, "utf8"))

            if requestMsg == "q":
                client.send(bytes(Request.CLOSE_CONNECTION, "utf8"))
                break
        except:
            print("Send error.")
            client.close()


clientThread = Thread(target=receive)
clientThreadSend = Thread(target=send)
clientThread.start()
clientThreadSend.start()