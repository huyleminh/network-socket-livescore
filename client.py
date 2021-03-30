import socket
import threading

IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

Thread = threading.Thread

HOST = "127.0.0.1"
PORT = 3000

# Client socket
client = socket.socket(IPV4, TCP)
client.connect((HOST, PORT))
print("Connect successfully")

# def sendMsg():
#     global client
#     try:
#         while True:
#             data = client.recv(1024)
#             print('Server:', data.decode("utf8"))

#             msg = input('Client: ')
#             client.send(bytes(msg, "utf8"))

#             if msg == "q":
#                 break
#     finally:
#         print('Client closed')
#         client.close()

def receive():
    while True:
        try:
            msg = client.recv(1024).decode("utf8")
            print("Receive: " + msg)
            if msg == "q":
                break
        except OSError:
            break



def send():
    try:
        while True:
            msg = input('Client: ')
            client.send(bytes(msg, "utf8"))

            if msg == "q":
                break
    except:
        print('Client closed')
        client.close()
    finally:
        print('Client closed')
        client.close()


clientThread = Thread(target=receive)
clientThreadSend = Thread(target=send)
clientThread.start()
clientThreadSend.start()