import sys
from pathlib import Path

pathfile = Path(__file__).resolve()
utilsRoot = pathfile.parents[1]
sys.path.append(str(utilsRoot))

from db.DBHandler import DBHandler

class Authentication:
    @staticmethod
    def checkLogin(userInfo=None):
        if not userInfo:
            return False

        users = DBHandler.readAllUsers()
        for user in users:
            if userInfo == user:
                return True
        return False