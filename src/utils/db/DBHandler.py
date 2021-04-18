import json

class DBHandler:
    @staticmethod
    def readAllUsers():
        FUsers = open("database/Users.json")

        users = FUsers.read()
        usersJSON = json.loads(users)
        FUsers.close()
        return usersJSON

    @staticmethod
    def writeAllUsers(usersJSON):
        with open("database/Users.json", "w") as write_file:
            json.dump(usersJSON, write_file)
            write_file.close()