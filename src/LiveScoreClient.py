import socket
import threading
import json
import time

from shared.Message import Login

IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

Thread = threading.Thread

HOST = "127.0.0.1"
PORT = 3000

# Client socket
client = socket.socket(IPV4, TCP)
client.connect((HOST, PORT))
print("Connect successfully")

login = False

def receive():
    global login
    try:
        # ? Try to login
        while login == False:
            msg = client.recv(1024).decode("utf8")

            if msg == Login.SUCCESS:
                print("Login successfully.")
                login = True
            elif msg == Login.FAILED:
                print("Unable to login, please try again.")
                login = False
            elif msg == "ExcessConnection": #msg indicate that there are too many connection, force close
                client.close()
                break

        # Listen response from server
        while True:
            msg = client.recv(1024).decode("utf8")
            if len(msg) > 0:
                print("Receive: " + msg)

                if msg == "qUiTqUiT":
                    client.close()
                    break

    except OSError:
        client.close()

def send():
    global login
    try:
        # ? Try to login
        while login == False:
            username = input("Username: ")
            password = input("Password: ")

            userInfo = { "username": username, "password": password }
            client.send(bytes(json.dumps(userInfo), "utf8"))
            time.sleep(0.1)

        while True:
            requestMsg = input("Request: ")
            if len(requestMsg) == 0:
                continue

            client.send(bytes(requestMsg, "utf8"))

            if requestMsg == "q":
                break
    except:
        print('Error, client closed.')
        client.close()


clientThread = Thread(target=receive)
clientThreadSend = Thread(target=send)
clientThread.start()
clientThreadSend.start()