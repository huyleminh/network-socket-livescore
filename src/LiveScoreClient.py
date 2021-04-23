import json
import math
import socket
import sys
import threading
import time
from functools import partial
from tkinter import *
from tkinter import messagebox

from shared.ConstSock import ConstSock
from shared.Message import Login, Request, Response
from views.HomeView import *
from views.Login import *
from views.Logout import *
from views.MatchDetailsView import *
from views.MatchView import *
from views.Register import *

Thread = threading.Thread
client = socket.socket(ConstSock.IP_ADDRESS, ConstSock.PROTOCOL)
client.connect((ConstSock.HOST_IP, ConstSock.DEFAULT_PORT))

login = { "status": False, "role": ""}
connected = False
denny = False
layouts = {}
msgRT = ""

def realTime(client):
    global msgRT
    while True:
        temp1 = client.recv(1024).decode("utf8")
        msgRT += temp1
        if len(temp1) != 1024:
            break
    msgRT = json.loads(msgRT)

def receive():
    global login, connected, denny
    try:
        msg =  client.recv(1024).decode("utf8")

        if msg == Response.EXCESS_CONNECTION: #msg indicate that there are too many connections, force close
            denny = True
            messagebox.showerror("Error detected", "Connection denied, queue is overflow. Please try again later.")
        elif msg == Response.SUCCESS_CONNECTION:
            connected = True
            print("Connect successfully.")

        # Done: connect sucessfully
        while connected == True: # ? Try to login
            while login["status"] == False:
                mode = client.recv(1024).decode("utf8") # determine accepted mode from server
                if mode == Response.CLOSE_CONNECTION: # raise an error when choosing mode
                    raise Exception("Choose mode failed")
                elif mode == Request.LOGIN_MODE:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        login = { "status": True, "role": "client"}
                        layouts["login"].destroy()
                        messagebox.showinfo("Notification", "Login successfully, welcome CLIENT.")
                        break
                    elif msg == Login.ADMIN_ACCESS:
                        login = { "status": True, "role": "admin"}
                        layouts["login"].destroy()
                        messagebox.showinfo("Notification", "Login successfully, welcome ADMIN.")
                    elif msg == Login.FAILED:
                        layouts["login"].destroy()
                        messagebox.showwarning("Alert", "Unable to login, please try again.")
                elif mode == Request.REGISTER_MODE:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        login = { "status": True, "role": "client"}
                        layouts["register"].destroy()
                        messagebox.showinfo("Notification","Register successfully.")
                        break
                    elif msg == Login.FAILED:
                        layouts["register"].destroy()
                        messagebox.showwarning("Alert","Account existed.")

            msg = ""
            while True:
                temp = client.recv(1024).decode("utf8")
                msg += temp
                if len(temp) != 1024:
                    break
            msg = json.loads(msg)
            if msg["code"] == Response.CLOSE_CONNECTION:
                break
            elif msg["code"] == Response.VIEW_ALL_MATCHES:
                allMatchView(client, msg["data"])
            elif msg["code"] == Response.VIEW_MATCH_BY_ID:
                response = msg["data"]
                if response["status"] == 200:
                    detailMatchView(response["data"])
            elif msg["code"] == Response.REAL_TIME_MODE_INIT:
                realTimeView(client, msg["data"])
            elif msg["code"] == Response.REAL_TIME_MODE:
                global msgRT
                tempThread = Thread(target=realTime, args=(client,))
                tempThread.start()
                while True:
                    time.sleep(1)
                    client.send(bytes(json.dumps({ "code": Request.REAL_TIME_MODE }), "utf8"))
                    if msgRT["code"] == Response.HALT_RT_MODE:
                        break
                    allMatchView(client, msg["data"])
                    #realTimeView(client, msgRT["data"])
            #elif msg["code"] == Response.HALT_RT_MODE:


        client.close()
    except Exception:
        connected = False
        client.close()
    except:
        print("Server error detected. Press enter to close connection.")
        connected = False
        client.close()

clientThread = Thread(target=receive)
clientThread.start()


def toggleHome():
    if login["status"] == False:
        messagebox.showwarning("Alert", "You have to login first")
        return
    else:
        homeView(mainScreen, layouts, client, login["role"])

def toggleLogin():
    if login["status"]:
        messagebox.showinfo("Notification", "You are already logged in")
        return
    else:
        loginView(mainScreen, client, layouts)

def toggleLogout():
    if not login["status"]:
        messagebox.showwarning("Alert", "You are not logged in")
    else:
        logoutProcess(client, layouts)

def onCloseWindow():
    try:
        client.send(bytes(json.dumps({ "code" : Request.CLOSE_CONNECTION }), "utf8"))
    except:
        messagebox.showerror("Error", "Connection error")
        layouts["mainScreen"].destroy()
        return
    layouts["mainScreen"].destroy()

mainScreen = Tk()
mainScreen.title("Main screen")
mainScreen.configure(bg="#000000")

layouts["mainScreen"] = mainScreen

WIDTH = mainScreen.winfo_screenwidth()
HEIGHT = mainScreen.winfo_screenheight()
PADDING_LEFT = math.ceil(WIDTH / 4)
PADDING_TOP = math.ceil(HEIGHT / 8)
mainScreen.geometry(str(math.ceil(WIDTH / 2)) + "x" + str(math.ceil(HEIGHT / 2)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))

if not denny: # Success connection
    Label(mainScreen, text="Welcome To LiveScore For Client", bg="#000000", width=110, height=2, font=(14), fg="#ff9017").grid(row=0, columnspan=4, sticky="we")

    Button(mainScreen, text="Choose features", height=2, width=34, activebackground="#363636", command=toggleHome, bg="#212121", fg="#ff9017").grid(row=1, column=0, sticky="w")
    Button(mainScreen, text="Login", height=2, width=34, activebackground="#363636", command=toggleLogin, bg="#212121", fg="#ff9017").grid(row=1, column=1, sticky="w")
    Button(mainScreen, text="Register", height=2, width=34, activebackground="#363636", command=partial(toggleRegister, mainScreen, client, layouts), bg="#212121", fg="#ff9017").grid(row=1, column=2, sticky="w")
    Button(mainScreen, text="Logout", height=2, width=34, activebackground="#363636", command=toggleLogout, bg="#212121", fg="#ff9017").grid(row=1, column=3, sticky="w")

    Label(mainScreen, text="© Copyright 2021 - Developed by Huy Le Minh and Hung Nguyen Hua",bg="#000000", font=(10), fg="#ff9017", justify=CENTER).grid(sticky="swe", row=3, columnspan=4)

    mainScreen.rowconfigure(3, weight=1)
    mainScreen.protocol("WM_DELETE_WINDOW", onCloseWindow)
    mainScreen.mainloop()
