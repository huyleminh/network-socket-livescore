import json
import math
import sys
from functools import partial
from pathlib import Path
from tkinter import *
from tkinter import messagebox

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request


def logoutProcess(client, layouts):
    try:
        client.send(bytes(json.dumps({ "code": Request.CLOSE_CONNECTION }), "utf8"))
        messagebox.showinfo("Notification", "Thank you, see you again")
        layouts["mainScreen"].destroy()
    except:
        messagebox.showerror("Error", "Connection error")
        layouts["mainScreen"].destroy()
