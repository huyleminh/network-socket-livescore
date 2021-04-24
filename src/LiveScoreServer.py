import json
import socket
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk

from shared.ConstSock import ConstSock
from shared.Message import Login, Request, Response
from utils.auth.Authentication import Authentication
from utils.db.DBHandler import DBHandler
from utils.db.details.DBDetailsHandler import DBDetailsHandler
from utils.db.matches.DBMatchesHandler import DBMatchesHandler
from utils.message.Message import *

Thread = threading.Thread
server = socket.socket(ConstSock.IP_ADDRESS, ConstSock.PROTOCOL)
server.bind((ConstSock.HOST_IP, ConstSock.DEFAULT_PORT))
server.listen(ConstSock.MAX_CLIENTS)

userConnections = []
addresses = []
n = 0 #client counter
rowsCounter = 1

def mainThreadServerSide():
    global server, addresses, n, rowsCounter
    while True:
        try:
            if n != ConstSock.MAX_CLIENTS:
                connection, address = server.accept()

                # Send success response to client
                connection.send(bytes(Response.SUCCESS_CONNECTION, "utf8"))
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Connected", "", "New connection", datetime.now()))

                addresses.append(address)
                n = n + 1
                rowsCounter += 1

                Thread(target=clientThreadServerSide, args=(connection, address)).start()
            else: #handle more connections than max_connections case
                connection, address = server.accept()
                if n != ConstSock.MAX_CLIENTS:
                    # Send success response to client
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Connected", "", "New connection", datetime.now()))
                    connection.send(bytes(Response.SUCCESS_CONNECTION, "utf8"))

                    addresses.append(address)
                    n = n + 1
                    rowsCounter += 1

                    Thread(target=clientThreadServerSide, args=(connection, address)).start()
                else:
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Dennied", "", "New connection", datetime.now()))
                    rowsCounter += 1

                    connection.send(bytes(Response.EXCESS_CONNECTION, "utf8")) #send msg to force client close connection immediately
                    time.sleep(0.1)
                    connection.close()

        except:
            break

def clientThreadServerSide(connection, address):
    global userConnections, n, rowsCounter
    userConnections.append(connection)

    try:
        while True:
            userInfo = connection.recv(1024).decode("utf8") #Listen for mode request from client
            userInfo = json.loads(userInfo)

            if userInfo["code"] == Request.LOGIN_MODE: #Client request login mode
                connection.send(bytes(json.dumps({ "code": Request.LOGIN_MODE }), "utf8"))

            elif userInfo["code"] == Request.REGISTER_MODE:
                connection.send(bytes(json.dumps({ "code": Request.REGISTER_MODE }), "utf8"))

            elif userInfo["code"] == Request.CLOSE_CONNECTION:
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Disconnected", Request.CLOSE_CONNECTION, "Interrupt", datetime.now()))
                rowsCounter += 1

                connection.send(bytes(json.dumps({ "code": Response.CLOSE_CONNECTION }), "utf8"))
                raise Exception("Client interrupted")

            if userInfo["code"] == Request.LOGIN_MODE: #Client request login mode
                userInfo = connection.recv(1024).decode("utf8")
                auth = Authentication.checkLogin(json.loads(userInfo))

                if auth["status"] == True:
                    if auth["role"] == "client":
                        connection.send(bytes(Login.SUCCESS, "utf8"))
                    elif auth["role"] == "admin":
                        connection.send(bytes(Login.ADMIN_ACCESS, "utf8"))
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Verified", Request.LOGIN_MODE, "Login request", datetime.now()))
                    rowsCounter += 1
                    break

                else:
                    connection.send(bytes(Login.FAILED, "utf8"))
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Failed", Request.LOGIN_MODE, "Login request", datetime.now()))
                    rowsCounter += 1

            elif userInfo["code"] == Request.REGISTER_MODE: #Client request register mode
                userInfo = connection.recv(1024).decode("utf8")
                auth = Authentication.checkRegister(json.loads(userInfo))

                if auth == True:
                    connection.send(bytes(Login.FAILED, "utf8"))
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Failed", Request.REGISTER_MODE, "Register request", datetime.now()))
                    rowsCounter += 1
                else:
                    Authentication.registerNew(json.loads(userInfo))
                    connection.send(bytes(Login.SUCCESS, "utf8"))
                    serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Success", Request.LOGIN_MODE, "Register request", datetime.now()))
                    rowsCounter += 1
                    break

        # Done: Login Success
        while True:
            res = connection.recv(1024).decode("utf8")
            res = json.loads(res)

            if res["code"] == Request.CLOSE_CONNECTION:
                connection.send(bytes(json.dumps({ "code": Response.CLOSE_CONNECTION }), "utf8"))
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Disconnected", Request.CLOSE_CONNECTION, "Close connection", datetime.now()))
                rowsCounter += 1

                connection.close()
                userConnections.remove(connection)
                addresses.remove(address)
                n = n - 1
                break

            if res["code"] == Request.VIEW_ALL_MATCHES:
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Ok", Request.VIEW_ALL_MATCHES, "View all matches", datetime.now()))
                rowsCounter += 1

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
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Ok", Request.VIEW_MATCH_BY_ID, "View match details", datetime.now()))
                rowsCounter += 1

            if res["code"] == Request.REAL_TIME_MODE:
                response = DBMatchesHandler.getAllMatches()
                matches = []
                if response["status"] == 500:
                    matches = []
                elif response["status"] == 200:
                    matches = response["data"]
                connection.send(bytes(json.dumps({ "code": Response.REAL_TIME_MODE, "data": matches }),"utf8"))
                serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Ok", Request.REAL_TIME_MODE, "View all matches - Real time", datetime.now()))
                rowsCounter += 1

    except: #Client suddenly drops connection
        serverTreeView.insert("", "end", text=rowsCounter, values=(address[0], address[1], "Connection error", "", "", datetime.now()))
        rowsCounter += 1
        connection.close()
        userConnections.remove(connection)
        addresses.remove(address)
        n = n - 1

serverView = Tk()
serverTreeView = ttk.Treeview(serverView)

def disconectAll():
    global userConnections, addresses

    if len(userConnections) == 0 or len(addresses) == 0:
        messagebox.showinfo("Notification", "No connections available")
        return

    confirm = messagebox.askquestion("Disconection warning", "Are you sure about closing all connections")
    if confirm == "yes":
        sendAllMessage(Response.FORCE_CLOSE_CONNECTION, userConnections)

def onCloseWindow():
    messagebox.showwarning("Warning", "You can not shut the server down by this way")

if __name__ == "__main__":
    serverThread = Thread(target=mainThreadServerSide)
    serverThread.start()

    # Set window size and title
    serverView.geometry("1020x400+0+150")
    serverView.title("Server application")

    Label(serverView, text="Server started at " + str(datetime.now()))

    serverScrollbar = ttk.Scrollbar(serverView, orient=VERTICAL, command=serverTreeView.yview)
    serverScrollbar.pack(side=RIGHT, fill=X)

    # Styles:
    styles = ttk.Style(serverView)
    styles.theme_use("clam")
    styles.configure("Treeview", rowheight=30)
    styles.map("Treeview", background=[("selected", "#2433d6")])

    # Table configuration:
    serverTreeView["columns"] = ("IPAddress", "Port", "Status", "RequestCode", "RequestText", "Time")

    serverTreeView.column("#0", anchor=CENTER, width=40, minwidth=40)
    serverTreeView.column("IPAddress", anchor=CENTER, width=150, minwidth=150)
    serverTreeView.column("Port", anchor=CENTER, width=60, minwidth=50)
    serverTreeView.column("Status", anchor=CENTER, width=100, minwidth=100)
    serverTreeView.column("RequestCode", anchor=CENTER, width=120, minwidth=120)
    serverTreeView.column("RequestText", anchor=CENTER, width=100, minwidth=100)
    serverTreeView.column("Time", anchor=CENTER, width=200, minwidth=150)

    serverTreeView.heading("#0", text="No", anchor=CENTER)
    serverTreeView.heading("IPAddress", text="IP Address", anchor=CENTER)
    serverTreeView.heading("Port", text="Port", anchor=CENTER)
    serverTreeView.heading("Status", text="Status", anchor=CENTER)
    serverTreeView.heading("RequestCode", text="Request Code", anchor=CENTER)
    serverTreeView.heading("RequestText", text="Request Text", anchor=CENTER)
    serverTreeView.heading("Time", text="Time", anchor=CENTER)

    serverTreeView.pack(fill=BOTH)

    Button(serverView, text="Disconnect all clients", bg="#e21818", fg="#ffffff", activebackground="#e02c2c", activeforeground="#ffffff", height=1, padx=2, pady=2, command=disconectAll).pack()

    serverView.protocol("WM_DELETE_WINDOW", onCloseWindow)

    serverView.mainloop()

    serverThread.join()
    server.close() # Close after thread died
