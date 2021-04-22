import sys
from pathlib import Path

pathfile = Path(__file__).resolve()
utilsRoot = pathfile.parents[1]
sys.path.append(str(utilsRoot))

from db.DBHandler import DBHandler

class Authentication:
    @staticmethod
    def checkLogin(userInfo):
        users = DBHandler.readAllUsers()
        for user in users:
            if userInfo["username"] == user["username"] and userInfo["password"] == user["password"]:
                return { "status": True, "role": user["role"] }
        return { "status": False }

    @staticmethod
    def checkRegister(userInfo=None):
        if not userInfo:
            return False

        users = DBHandler.readAllUsers()
        for user in users:
            if userInfo["username"] == user["username"]:
                return True
        return False
    
    @staticmethod
    def registerNew(userInfo=None):
        if not userInfo:
            return False

        users = DBHandler.readAllUsers()
        users.append(userInfo)
        DBHandler.writeAllUsers(users)
        return True