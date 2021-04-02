from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

host = "127.0.0.1"
port = 33000

address = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

server.listen(1)

print("Waiting...")

connect, ip = server.accept()

username = ""
password = ""

try:
    print("Connected by: ", ip)
    while True:
        i = 0
        msg = connect.recv(1024)
        if len(msg) > 0:
            if i == 0:
                username = msg.decode("utf8")
                i += 1
            else:
                password = msg.decode("utf8")
                break
                """f = open("../Account/account_list.txt", "rt")
                flag = False
                for x in f:
                    if username == x:
                        if password == f.readline():
                            connect.send(bytes("Correct info", "utf8"))
                            flag = True
                if flag == False:
                    connect.send(bytes("Incorrect info", "utf8"))"""
            #print("Server receive: " + msg.decode("utf8"))
        print(username + " " + password)
except KeyboardInterrupt:
    connect.close()
finally:
    connect.close()