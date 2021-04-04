import json

class DBHandler:
    @staticmethod
    def readAllUsers():
        FUsers = open("database/Users.json")

        users = FUsers.read()
        usersJSON = json.loads(users)
        return usersJSON