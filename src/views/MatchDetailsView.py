import json
import math
from tkinter import *
from tkinter import ttk


def detailMatchView(dataDetail):
    detailView = Tk()
    detailView.title("View details")
    WIDTH = detailView.winfo_screenwidth()
    HEIGHT = detailView.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 3)
    PADDING_TOP = math.ceil(HEIGHT / 4)
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
            homeScore = 0
            awayScore = 0

        events = details["events"]
        for i in range(0, len(events)):
            event = events[i]
            homePlayer = ""
            awayPlayer = ""

            player = event["player"]
            if event["assist"] != "null":
                player += "(Assist: " + event["assist"] + ")"
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