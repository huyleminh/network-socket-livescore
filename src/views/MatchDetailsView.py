import json
import math
from tkinter import *
from tkinter import ttk


def detailMatchView(dataDetail):
    detailView = Tk()
    detailView.title("View details")
    detailView.configure(bg="#000000")

    match = dataDetail["match"]
    homeScore = match["homeScore"]
    awayScore = match["awayScore"]

    styles = ttk.Style(detailView)
    styles.theme_use("default")
    styles.configure("Treeview", background="#000000", fieldbackground="#000000", rowheight=30)
    styles.map("Treeview", background=[("selected", "#414141")], foreground=[("selected", "#ff8300"), ("!selected", "#f48f29")])

    treeDetails = ttk.Treeview(detailView)
    scrollbar = ttk.Scrollbar(detailView, orient=VERTICAL, command=treeDetails.yview)
    scrollbar.pack(side="right", fill="x")

    treeDetails["columns"] = ("Time", "Home", "Event", "Away")

    treeDetails.column("#0", anchor=CENTER, width=40, minwidth=40)
    treeDetails.column("Time", anchor=CENTER, width=60, minwidth=40)
    treeDetails.column("Home", anchor=CENTER, width=250, minwidth=100)
    treeDetails.column("Event", anchor=CENTER, width=100, minwidth=100)
    treeDetails.column("Away", anchor=CENTER, width=250, minwidth=100)

    treeDetails.heading("#0", text="No", anchor=CENTER)
    treeDetails.heading("Time", text="Time", anchor=CENTER)
    treeDetails.heading("Home", text="Home", anchor=CENTER)
    treeDetails.heading("Event", text="", anchor=CENTER)
    treeDetails.heading("Away", text="Away", anchor=CENTER)

    treeDetails.pack(fill=BOTH)

    result = match["homeScore"] + " - " + match["awayScore"]
    treeDetails.insert("", "end", text="", values=(match["status"], match["home"], result, match["away"]))
    treeDetails.insert("", "end", text="", values=("", "", "", ""))

    if dataDetail["details"] != {}:
        details = dataDetail["details"]

        if homeScore != "?" and awayScore != "?":
            homeScore = awayScore = 0

        events = details["events"]

        for i in range(0, len(events)):
            event = events[i]
            homePlayer = awayPlayer = ""

            player = event["player"]
            if event["assist"] != "null":
                player += " (Assist: " + event["assist"] + ")"
            if event["team"] == "home":
                homePlayer = player
                if event["type"] == "goal":
                    homeScore += 1
                    result = str(homeScore) + " - " + str(awayScore)
                else:
                    result = event["type"]
            else:
                awayPlayer = player
                if event["type"] == "goal":
                    awayScore += 1
                    result = str(homeScore) + " - " + str(awayScore)
                else:
                    result = event["type"]
            treeDetails.insert("", "end", text=i + 1, values=(event["time"], homePlayer, result, awayPlayer))

    detailView.mainloop()


def editMatchDetail(dataDetail):
    def onDoubleClick():
        selected = treeDetails.focus()
        values = treeDetails.item(selected, "values")
        box1.delete(0, END)
        box2.delete(0, END)
        box3.delete(0, END)
        box4.delete(0, END)
        box1.insert(0, values[0])
        box2.insert(0, values[1])
        box3.insert(0, values[2])
        box4.insert(0, values[3])
    def save():
        selected = treeDetails.focus()
        values = treeDetails.item(selected, text="", values=(box1.get(), box2.get(), box3.get(), box4.get()))
        box1.delete(0, END)
        box2.delete(0, END)
        box3.delete(0, END)
        box4.delete(0, END)
    
    detailView = Tk()
    detailView.title("Edit details")
    detailView.configure(bg="#000000")

    match = dataDetail["match"]
    homeScore = match["homeScore"]
    awayScore = match["awayScore"]

    styles = ttk.Style(detailView)
    styles.theme_use("default")
    styles.configure("Treeview", background="#000000", fieldbackground="#000000", rowheight=30)
    styles.map("Treeview", background=[("selected", "#414141")], foreground=[("selected", "#ff8300"), ("!selected", "#f48f29")])

    treeDetails = ttk.Treeview(detailView)
    scrollbar = ttk.Scrollbar(detailView, orient=VERTICAL, command=treeDetails.yview)
    scrollbar.pack(side="right", fill="x")

    treeDetails["columns"] = ("Time", "Home", "Event", "Away")

    treeDetails.column("#0", anchor=CENTER, width=40, minwidth=40)
    treeDetails.column("Time", anchor=CENTER, width=60, minwidth=40)
    treeDetails.column("Home", anchor=CENTER, width=250, minwidth=100)
    treeDetails.column("Event", anchor=CENTER, width=100, minwidth=100)
    treeDetails.column("Away", anchor=CENTER, width=250, minwidth=100)

    treeDetails.heading("#0", text="No", anchor=CENTER)
    treeDetails.heading("Time", text="Time", anchor=CENTER)
    treeDetails.heading("Home", text="Home", anchor=CENTER)
    treeDetails.heading("Event", text="", anchor=CENTER)
    treeDetails.heading("Away", text="Away", anchor=CENTER)

    treeDetails.pack(fill=BOTH)

    result = match["homeScore"] + " - " + match["awayScore"]
    treeDetails.insert("", "end", text="", values=(match["status"], match["home"], result, match["away"]))
    treeDetails.insert("", "end", text="", values=("", "", "", ""))

    if dataDetail["details"] != {}:
        details = dataDetail["details"]

        if homeScore != "?" and awayScore != "?":
            homeScore = awayScore = 0

        events = details["events"]

        for i in range(0, len(events)):
            event = events[i]
            homePlayer = awayPlayer = ""

            player = event["player"]
            if event["assist"] != "null":
                player += " (Assist: " + event["assist"] + ")"
            if event["team"] == "home":
                homePlayer = player
                if event["type"] == "goal":
                    homeScore += 1
                    result = str(homeScore) + " - " + str(awayScore)
                else:
                    result = event["type"]
            else:
                awayPlayer = player
                if event["type"] == "goal":
                    awayScore += 1
                    result = str(homeScore) + " - " + str(awayScore)
                else:
                    result = event["type"]
            treeDetails.insert("", "end", text=i + 1, values=(event["time"], homePlayer, result, awayPlayer))
    
    treeDetails.bind("<Double-1>", onDoubleClick)

    box1 = Entry(detailView, width=40)
    box2 = Entry(detailView, width=40)
    box3 = Entry(detailView, width=40)
    box4 = Entry(detailView, width=40)

    my_button= Button(detailView, text= "Save", command=save)
    my_button1= Button(detailView, text= "Select to edit", command=onDoubleClick)
    

    box1.pack()
    box2.pack()
    box3.pack()
    box4.pack()
    my_button1.pack(pady=5)
    my_button.pack(pady=5)

    detailView.mainloop()