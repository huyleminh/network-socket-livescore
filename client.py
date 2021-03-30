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
def sendMsg():
    global client
    try:
        while True:
            msg = input('Client: ')
            client.sendall(bytes(msg, "utf8"))

            if msg == "q":
                break

            data = client.recv(1024)
            print('Server:', data.decode("utf8"))
    finally:
        print('Client closed')
        client.close()

clientThread = Thread(target=sendMsg)
clientThread.start()