from tkinter import *
from tkinter import messagebox
import sys, math, json
from pathlib import Path
from functools import partial

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request

def logoutProcess(client, layouts):
    messagebox.showinfo("Notification", "Thank you, see you again")
    client.send(bytes(json.dumps({ "code": Request.CLOSE_CONNECTION }), "utf8"))
    layouts["mainScreen"].destroy()
