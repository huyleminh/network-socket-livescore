from tkinter import *
import sys, math, json
from pathlib import Path
from functools import partial

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request


def sendRegister(client, username, password):
    client.send(bytes(Request.REGISTER_MODE, "utf8"))
    u = username.get()
    p = password.get()
    userInfo = { "username": u, "password": p, "role": "client"}
    client.send(bytes(json.dumps(userInfo), "utf8"))

    username.set("")
    password.set("")

def toggleRegister(mainScreen, client, layouts):
    registerScreen = Toplevel(mainScreen)
    registerScreen.title("Register screen")
    WIDTH = mainScreen.winfo_screenwidth()
    HEIGHT = mainScreen.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 4)
    PADDING_TOP = math.ceil(HEIGHT / 8)
    registerScreen.geometry(str(math.ceil(WIDTH / 4)) + "x" + str(math.ceil(HEIGHT / 4)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))

    username = StringVar()
    password = StringVar()

    usenameLabel = Label(registerScreen, text="Username").grid(row=0, column=0)
    usernameEntry = Entry(registerScreen, textvariable=username, width=40).grid(row=0, column=1)

    passwordLabel = Label(registerScreen, text="Password").grid(row=1, column=0)
    passwordEntry = Entry(registerScreen, textvariable=password, show="*", width=40).grid(row=1, column=1)

    registerSubmit = Button(registerScreen, text="Register", width=10, height=1, bg="#46a049", fg="#ffffff", command=partial(sendRegister, client, username, password)).grid(row=2, column=1)
    layouts["register"] = registerScreen

    registerScreen.mainloop()