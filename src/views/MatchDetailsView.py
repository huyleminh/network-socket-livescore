import json
import math
from tkinter import *


def detailMatchView(dataDetail):
    detailView = Tk()
    detailView.title("Detail view")
    WIDTH = detailView.winfo_screenwidth()
    HEIGHT = detailView.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 3)
    PADDING_TOP = math.ceil(HEIGHT / 4)
    detailView.geometry(str(math.ceil(WIDTH / 3)) + "x" + str(math.ceil(HEIGHT / 3)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    detailView.configure(bg="#000000")

    match = dataDetail["match"]
    homeScore = match["homeScore"]
    awayScore = match["awayScore"]

    detailView.columnconfigure(0, weight=1)
    Label(detailView, text=match["status"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=0, column=0)

    detailView.columnconfigure(1, weight=1)
    Label(detailView, text=match["home"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=0, column=1)

    detailView.columnconfigure(2, weight=1)
    result = homeScore + " - " + awayScore
    Label(detailView, text=result, fg="#ff9017", bg="#000000").grid(row=0, column=2)

    detailView.columnconfigure(3, weight=1)
    Label(detailView, text=match["away"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=0, column=3)

    detailView.rowconfigure(1, weight=1)
    Label(detailView, text="               Events:", bg="#212121", fg="#ff9017", anchor="w").grid(row=1, columnspan=4, sticky="we")

    if dataDetail["details"] == {}:
        Label(detailView, text="No events detected", fg="#ff9017", anchor="center").grid(row=2, columnspan=4, sticky="we")
    else:
        details = dataDetail["details"]

        if homeScore != "?" and awayScore != "?":
            homeScore = awayScore = 0

        events = details["events"]
        for i in range(0, len(events)):
            event = events[i]
            detailView.rowconfigure(i + 2, weight=1)
            Label(detailView, text=event["time"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=0)

            player = event["player"]
            if event["assist"] != "null":
                player += "(Assist: " + event["assist"] + ")"

            if event["team"] == "home":
                Label(detailView, text= player, justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=1)
                if event["type"] == "goal":
                    homeScore += 1
                    Label(detailView, text=str(homeScore) + " - " + str(awayScore), justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=2)
                else:
                    Label(detailView, text=event["type"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=2)
            else:
                if event["type"] == "goal":
                    awayScore += 1
                    Label(detailView, text=str(homeScore) + " - " + str(awayScore), justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=2)
                else:
                    Label(detailView, text=event["type"], justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=2)
                Label(detailView, text= player, justify=CENTER, fg="#ff9017", bg="#000000").grid(row=i + 2, column=3)

    detailView.mainloop()
