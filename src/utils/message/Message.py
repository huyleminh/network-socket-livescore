import json

def sendAllMessage(message, userConnections):
    for userConnection in userConnections:
        if userConnection:
            userConnection.send(bytes(
                json.dumps({"code": message }),
                "utf8")
            )