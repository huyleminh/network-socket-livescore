import math
from functools import partial
from tkinter import *

def viewMatchByID(idMatch):
    pass

def allMatchView(data):
    view = Tk()
    WIDTH = view.winfo_screenwidth()
    HEIGHT = view.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 3)
    PADDING_TOP = math.ceil(HEIGHT / 4)
    view.geometry(str(math.ceil(WIDTH / 3)) + "x" + str(math.ceil(HEIGHT / 3)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    view.configure(bg="#000000")

    for i in range(0, len(data)):
        view.rowconfigure(i, weight=1)
        dataItem = data[i]
        view.columnconfigure(0, weight=1)
        Label(view, text=dataItem["status"], justify=CENTER, fg="#bebebe", bg="#000000").grid(row=i, column=0)

        view.columnconfigure(1, weight=1)
        Label(view, text=dataItem["home"], justify=CENTER, fg="#bebebe", bg="#000000").grid(row=i, column=1)

        view.columnconfigure(2, weight=1)
        result = dataItem["homeScore"] + " - " + dataItem["awayScore"]
        Label(view, text=result, fg="#bebebe", bg="#000000").grid(row=i, column=2)

        view.columnconfigure(3, weight=1)
        Label(view, text=dataItem["away"], justify=CENTER, fg="#bebebe", bg="#000000").grid(row=i, column=3)

        view.columnconfigure(4, weight=1)
        Button(
            view,
            text="Details",
            bg="#212121",
            fg="#bebebe",
            bd=1, width=15,
            height=1,
            pady=2,
            activebackground="#363636",
            activeforeground="#e8e3e3",
            command=partial(viewMatchByID, dataItem["idMatch"])
        ).grid(row=i, column=4)

    view.mainloop()
