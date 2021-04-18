import socket
import threading
import json
import time

from shared.Message import Login, Response

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
        while connected ==True:
            # ? Try to login
            while login == False:
                msg = client.recv(1024).decode("utf8")

                if msg == Login.SUCCESS:
                    print("Login successfully.")
                    login = True
                    break
                elif msg == Login.FAILED:
                    print("Unable to login, please try again.")
                    login = False

            # Listen response from server
            msg = client.recv(1024).decode("utf8")
            if len(msg) > 0:
                print("Receive: " + msg)

                if msg == Response.CLOSE_CONNECTION:
                    break

        client.close()
    except:
        print("Server error detected. Press enter to close connection.")
        connected = False
        client.close()

def send():
    global login, connected
    while connected == True:
        # ? Try to login
        while login == False:
            try:
                username = input("Username: ")
                password = input("Password: ")

                userInfo = { "username": username, "password": password }
                client.send(bytes(json.dumps(userInfo), "utf8"))
                time.sleep(0.1)
            except:
                client.close()

        try:
            requestMsg = input("Request: ")
            if len(requestMsg) == 0:
                continue

            if connected == False:
                break

            client.send(bytes(requestMsg, "utf8"))

            if requestMsg == "q":
                break
        except:
            print("Send error.")
            client.close()


clientThread = Thread(target=receive)
clientThreadSend = Thread(target=send)
clientThread.start()
clientThreadSend.start()