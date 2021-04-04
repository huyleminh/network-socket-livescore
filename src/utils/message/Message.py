def sendAllMessage(message, userConnections):
    for userConnection in userConnections:
        if userConnection:
            userConnection.send(bytes(message, "utf8"))