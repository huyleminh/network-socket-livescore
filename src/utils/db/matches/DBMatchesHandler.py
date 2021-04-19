import json
import shortuuid as shortId

class DBMatchesHandler:
    @staticmethod
    def getAllMatches():
        try:
            fMatches = open("database/Matches.json")
            matches = fMatches.read()
            fMatches.close()
        except:
            return { "status": 500 }

        matchesJSON = json.loads(matches)
        return { "status": 200, "data": matchesJSON }

    @staticmethod
    def getMatchById(idMatch):
        if idMatch == "":
            return { "status": 404 }

        res = DBMatchesHandler.getAllMatches()

        if res["status"] == 500:
            return { "status": 500 }

        if res["status"] == 200:
            dataMatches = res["data"]
            for i in range(0, len(dataMatches)):
                if dataMatches[i]["idMatch"] == idMatch:
                    return { "status": 200, "data": dataMatches[i] }

            return { "status": 404 }

    @staticmethod
    def writeAllMatches(matches):
        with open("database/Matches.json", "w") as writeFile:
            json.dumps(matches, writeFile)
            writeFile.close()

    @staticmethod
    def createNewMatch(matchInfo):
        """ matchInfo: dict type
        - home and away: required
        - status: FT, time (minutes), HT, Pospt, time (begin time: date type), default is current date
        - homeScore and awayScore: default is ?
        """
        if not isinstance(matchInfo, dict):
            return { "status": 400, "text": "Invalid type" }

        if "home" not in matchInfo or "away" not in matchInfo:
            return { "status": 400, "text": "Missing attribute" }

        newMatch = {
            "idMatch": shortId.random(length=10),
            "home": matchInfo["home"],
            "away": matchInfo["away"],
            "status": matchInfo["status"],
            "homeScore": matchInfo["homeScore"],
            "awayScore": matchInfo["awayScore"],
            "details": shortId.random(length=10)
        }

        # Insert to database
        res = DBMatchesHandler.getAllMatches()
        if res["status"] == 500:
            return { "status": 500, "text": "Internal error"}

        if res["status"] == 200:
            dataMatches = res["data"]
            dataMatches.append(newMatch)
            DBMatchesHandler.writeAllMatches(dataMatches)
            return { "status": 201,  "text": "Create new ok"}
