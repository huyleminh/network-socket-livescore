import json
import shortuuid as shortId

class DBDetailsHandler:
    @staticmethod
    def getAllDetails():
        try:
            f= open("database/Details.json")
            details = f.read()
            f.close()
        except:
            return { "status": 500 }

        detailsJSON = json.loads(details)
        return { "status": 200, "data": detailsJSON }

    @staticmethod
    def getDetailsById(idDetail, idMatch):
        if idDetail == "" or idMatch == "":
            return { "status": 404 }

        res = DBDetailsHandler.getAllDetails()

        if res["status"] == 500:
            return { "status": 500 }

        if res["status"] == 200:
            dataDetails = res["data"]
            for i in range(0, len(dataDetails)):
                if dataDetails[i]["idDetail"] == idDetail and dataDetails[i]["idMatch"] == idMatch:
                    return { "status": 200, "data": dataDetails[i] }

            return { "status": 404 }

    @staticmethod
    def writeAllDetails(details):
        with open("database/Details.json", "w") as writeFile:
            json.dumps(details, writeFile)
            writeFile.close()

    @staticmethod
    def createNewDetai(detailInfo):
        """
        detailInfo: dict type
        - idDetail, idMatch: required
        """
        pass