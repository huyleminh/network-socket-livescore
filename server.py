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

clients = {}
address = {}

def handleClients():
    global server, address
    i = 0
    while True:
        print("waiting new connection")
        clientConnect, clientAddress = server.accept()
        i += 1
        print("Connected by ", clientAddress)
        address[clientConnect] = clientAddress
        # try:
        #     while True:
        #         message = clientConnect.recv(1024).decode("utf8")
        #         if message == "quit":
        #             break
        #         print("Client: " + message)

        #         # Send back:
        #         response = input("Server: ")
        #         clientConnect.sendall(bytes(response, "utf8"))
        # finally:
        #     clientConnect.close()
        #     print("Server closed")
        #     break
        if i < 4:
            print("Start new thread")
            a = Thread(target=clientThread, args=(clientConnect, i))
            a.start()
            print(threading.activeCount())
            # print(threading.current_thread)
        # finally:
        else:
            break

def clientThread(client, idClient):
    global clients
    clients[client] = "Client" + str(idClient)
    while True:
        res = client.recv(1024)
        if res != bytes("q", "utf8"):
            for sock in clients:
                sock.send(res)
        else:
            client.send(bytes("q", "utf8"))
            client.close()
            del clients[client]
            for sock in clients:
                sock.sendall(bytes("Client %s has left the chat" % idClient, "utf8"))
            break



if __name__ == "__main__":
    print("Server is listening: ")
    serverThread = Thread(target=handleClients)
    serverThread.start()
    serverThread.join()
    server.close() # Close after thread died
    # handleClients()