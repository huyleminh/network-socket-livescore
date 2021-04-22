from tkinter import *
import sys, math, json
from pathlib import Path
from functools import partial

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request


def sendLogin(client, username, password):
    client.send(bytes(Request.LOGIN_MODE, "utf8"))
    u = username.get()
    p = password.get()
    userInfo = { "username": u, "password": p }
    client.send(bytes(json.dumps(userInfo), "utf8"))

    username.set("")
    password.set("")

def toggleLogin(mainScreen, client, layouts):
    loginScreen = Toplevel(mainScreen)
    loginScreen.title("Login screen")
    WIDTH = mainScreen.winfo_screenwidth()
    HEIGHT = mainScreen.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 4)
    PADDING_TOP = math.ceil(HEIGHT / 8)
    loginScreen.geometry(str(math.ceil(WIDTH / 4)) + "x" + str(math.ceil(HEIGHT / 4)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))

    username = StringVar()
    password = StringVar()

    usenameLabel = Label(loginScreen, text="Username").grid(row=0, column=0)
    usernameEntry = Entry(loginScreen, textvariable=username, width=40).grid(row=0, column=1)

    passwordLabel = Label(loginScreen, text="Password").grid(row=1, column=0)
    passwordEntry = Entry(loginScreen, textvariable=password, show="*", width=40).grid(row=1, column=1)

    loginSubmit = Button(loginScreen, text="Log in", width=10, height=1, bg="#46a049", fg="#ffffff", command=partial(sendLogin, client, username, password)).grid(row=2, column=1)
    layouts["login"] = loginScreen

    loginScreen.mainloop()