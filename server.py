import socket
import threading

IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

Thread = threading.Thread

HOST = ""
PORT = 3000

# Server socket
server = socket.socket(IPV4, TCP)
server.bind((HOST, PORT))
server.listen(5)

connections = []
addresses = []

def createClientThread():
    global server, addresses
    print("Waiting new connection")

    while True:
        try:
            connection, address = server.accept()
            print("Connected by ", address)
            addresses.append(address)
            Thread(target=clientThread, args=(connection, address)).start()
        except KeyboardInterrupt:
            break

def clientThread(connection, address):
    global connections
    connections.append(connection)
    connection.send(bytes("Welcome " + address[0], "utf8"))
    while True:
        res = connection.recv(1024).decode("utf8")
        print("Client send: ", res, " from ", address)
        if res != "q":
            sendAllMessage(res, connections)
        else:
            connection.send(bytes("qUiTqUiT", "utf8"))
            connection.close()
            connections.remove(connection)

            sendAllMessage(address[0] + " has left. ", connections)
            break

def sendAllMessage(msg, connections):
    for connection in connections:
        if connection:
            print("Can send")
            connection.send(bytes(msg, "utf8"))

if __name__ == "__main__":
    print("Server is listening... ")
    serverThread = Thread(target=createClientThread)
    serverThread.start()
    serverThread.join()
    server.close() # Close after thread died