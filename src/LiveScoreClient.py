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
from views.MatchView import *
from views.Register import *

Thread = threading.Thread
client = socket.socket(ConstSock.IP_ADDRESS, ConstSock.PROTOCOL)
client.connect((ConstSock.HOST_IP, ConstSock.DEFAULT_PORT))

login = False
connected = False
denny = False
layouts = {}

def receive():
    global login, connected, denny
    try:
        msg =  client.recv(1024).decode("utf8")
        if msg == Response.EXCESS_CONNECTION: #msg indicate that there are too many connection, force close
            denny = True
            messagebox.showerror("Error detected", "Connection denied, queue is overflow. Please try again later.")
        elif msg == Response.SUCCESS_CONNECTION:
            connected = True
            print("Connect successfully.")

        # Done: connect sucessfully
        while connected == True: # ? Try to login
            while login == False:
                mode = client.recv(1024).decode("utf8") # determine accepted mode from server
                if mode == Response.CLOSE_CONNECTION: # raise an error when chosing mode
                    raise Exception("Chose mode failed")
                elif mode == Request.LOGIN_MODE:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        login = True
                        layouts["login"].destroy()
                        messagebox.showinfo("Alert", "Login successfully")
                        break
                    elif msg == Login.FAILED:
                        login = False
                        layouts["login"].destroy()
                        messagebox.showwarning("Alert", "Unable to login, please try again.")
                elif mode == Request.REGISTER_MODE:
                    msg = client.recv(1024).decode("utf8")

                    if msg == Login.SUCCESS:
                        login = True
                        layouts["register"].destroy()
                        messagebox.showinfo("Alert","Register successfully.")
                        break
                    elif msg == Login.FAILED:
                        login = False
                        messagebox.showwarning("Alert","Account existed.")
                        layouts["register"].destroy()
            msg = ""
            while True:
                temp = client.recv(1024).decode("utf8")
                msg += temp
                if len(temp) != 1024:
                    break
            if len(msg) > 0:
                if msg == Response.CLOSE_CONNECTION:
                    break
                else:
                    allMatchView(json.loads(msg))

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
    if login == False:
        messagebox.showwarning("Alert", "You have to login first")
        return
    else:
        homeView(mainScreen, layouts, client)

def toggleLogout():
    if not login:
        messagebox.showwarning("Alert", "You are not logged in")
    else:
        logoutProcess(client, layouts)

def onCloseWindow():
    try:
        client.send(bytes(Request.CLOSE_CONNECTION, "utf8"))
    except:
        messagebox.showerror("Error", "Server interrupted")
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

Label(mainScreen, text="Welcome to Livescore client", bg="#000000", width=110, height=2, font=(14), fg="#ff9017").grid(row=0, columnspan=4, sticky="we")

Button(mainScreen, text="Go to home", height=2, width=34, command=toggleHome, bg="#212121", fg="#ff9017").grid(row=1, column=0, sticky="w")
Button(mainScreen, text="Login", height=2, width=34, command=partial(toggleLogin, mainScreen, client, layouts), bg="#212121", fg="#ff9017").grid(row=1, column=1, sticky="w")
Button(mainScreen, text="Register", height=2, width=34, command=partial(toggleRegister, mainScreen, client, layouts), bg="#212121", fg="#ff9017").grid(row=1, column=2, sticky="w")
Button(mainScreen, text="Logout", height=2, width=34, command=toggleLogout, bg="#212121", fg="#ff9017").grid(row=1, column=3, sticky="w")

Label(mainScreen, text="© Copyright 2021 by Huy Le Minh and Hung Nguyen Hua",bg="#000000", font=(10), fg="#ff9017", justify=CENTER).grid(sticky="swe", row=3, columnspan=4)

mainScreen.columnconfigure(3, weight=1)
mainScreen.rowconfigure(2, weight=1)
mainScreen.protocol("WM_DELETE_WINDOW", onCloseWindow)

if not denny: # Success connection
    mainScreen.mainloop()
