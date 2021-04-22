import math
import sys
from functools import partial
from pathlib import Path
from tkinter import *

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request


def viewAllMatch(client):
    client.send(bytes(Request.VIEW_ALL_MATCHES, "utf8"))

def backToMain(layouts):
    layouts["homeScreen"].destroy()

def homeView(mainScreen, layouts, client):
    homeScreen = Toplevel(mainScreen)
    WIDTH = homeScreen.winfo_screenwidth()
    HEIGHT = homeScreen.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 4)
    PADDING_TOP = math.ceil(HEIGHT / 8)
    homeScreen.geometry(str(math.ceil(WIDTH / 2)) + "x" + str(math.ceil(HEIGHT / 2)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    homeScreen.configure(bg="#000000")
    layouts["homeScreen"] = homeScreen

    searchID = StringVar()

    Label(homeScreen, text="Welcome client", bg="#000000", height=2, font=(14), fg="#ff9017").grid(row=0, columnspan=2, sticky="we")

    Button(
        homeScreen,
        text="View all match",
        height=2, width=20,
        bg="#212121",
        fg="#bebebe",
        activebackground="#363636",
        activeforeground="#e8e3e3",
        command=partial(viewAllMatch, client)
    ).grid(row=1, column=0, sticky="nw")
    Button(
        homeScreen,
        text="Back",
        height=2,
        width=20,
        bg="#212121",
        fg="#bebebe",
        activebackground="#363636",
        activeforeground="#e8e3e3",
        command=partial(backToMain, layouts)
    ).grid(row=1, column=1, sticky="nw")

    homeScreen.columnconfigure(1, weight=1)
    homeScreen.rowconfigure(3, weight=1)

    homeScreen.mainloop()
