import math
import sys
import json
from functools import partial
from pathlib import Path
from tkinter import *

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request


def viewAllMatch(client):
    client.send(bytes(json.dumps({ "code": Request.VIEW_ALL_MATCHES }), "utf8"))

def backToMain(layouts):
    layouts["homeScreen"].destroy()

def homeView(mainScreen, layouts, client, role):
    homeScreen = Toplevel(mainScreen)
    WIDTH = homeScreen.winfo_screenwidth()
    HEIGHT = homeScreen.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 4)
    PADDING_TOP = math.ceil(HEIGHT / 8)
    homeScreen.geometry(str(math.ceil(WIDTH / 2)) + "x" + str(math.ceil(HEIGHT / 2)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    homeScreen.configure(bg="#000000")
    layouts["homeScreen"] = homeScreen

    searchID = StringVar()

    Label(homeScreen, text="Menu for " + role, bg="#000000", height=2, width=110, font=(14), fg="#ff9017", justify=CENTER).grid(row=0, columnspan=4, sticky="nwe")

    Button(
        homeScreen,
        text="View all matches",
        height=2, width=30,
        bg="#212121",
        fg="#ff9017",
        activebackground="#363636",
        activeforeground="#e8e3e3",
        command=partial(viewAllMatch, client)
    ).grid(row=1, column=0, sticky="w")

    if role == "admin":
        homeScreen.columnconfigure(1, weight=1)
        Button(
            homeScreen,
            text="Add new match",
            height=2,
            width=30,
            bg="#212121",
            fg="#ff9017",
            activebackground="#363636",
            activeforeground="#e8e3e3",
            # command=partial(backToMain, layouts)
        ).grid(row=1, column=1, sticky="w")

    Button(
        homeScreen,
        text="Real-time mode",
        height=2, width=30,
        bg="#212121",
        fg="#ff9017",
        activebackground="#363636",
        activeforeground="#e8e3e3",
        command=partial(viewAllMatch, client)
    ).grid(row=2, column=0, sticky="w")

    Button(
        homeScreen,
        text="Go Back",
        height=2,
        width=30,
        bg="#212121",
        fg="#ff9017",
        activebackground="#363636",
        activeforeground="#e8e3e3",
        command=partial(backToMain, layouts)
    ).grid(row=1, column=2, sticky="w")

    homeScreen.mainloop()
