### Importing Libraries
import pandas as pd
import requests
import time
import json
import copy
###



### RefSix API Class - Provides an endpoint for each of the API requests.
class RefsixApi:

## Class Setup
    _authenticationFile:JsonFile
    _apiSession:requests.Session
    
    _authenticatedUrl:str
    _authenticationExpires:int

    def __init__(self, filePath:str):
        """
        :param string filePath: The path to the file containing your RefSix login, API key, and other data, as seen in Example-Data/exampleInformation.json.
        """

        self._authenticationFile = JsonFile(filePath)
        self._apiSession = requests.Session()
##


## POST Login
    def POST_Login(self):
        (url, headers, payload) = self._FormatLoginRequest()

        start = time.time()
        response = self._apiSession.post(url, headers=headers, data=payload)
        print(f"POST Login: {response.status_code} {response.reason} - {round(time.time()-start, 2)} ms")

        if response.status_code == 200:
            self._authenticatedUrl = response.json()["userDBs"]["supertest"]
            self._authenticationExpires = response.json()["expires"]
        else:
            print(f"ERROR - status code '{response.status_code} {response.reason}' returned from POST Login.")


    def _FormatLoginRequest(self):
        authenticationData = self._authenticationFile.GetObjects({ "authentication": ["authentication"] })["authentication"]

        url = self._authenticationFile.GetAttributeValue("serverHost", ["hosts"])
        headers = { "Authentication": f"Bearer {authenticationData["authentication_key"]}", "Content-Type": "application/json" }
        payload = json.dumps({ "username": authenticationData["refsixUsername"], "password": authenticationData["refsixPassword"] })

        return (str(url), dict(headers), str(payload))
##


## GET All Matches
    def GET_AllMatches(self):
        """
        :return: A dict containing the list of matches.
        """
        if self._authenticationExpires <= time.time():
            print(f"ERROR - status code '401 Unauthorised' returned from GET All Matches. Run POST Login first.")
        
        (url, headers, payload) = self._FormatAllMatchesRequest()

        start = time.time()
        response = self._apiSession.get(url, headers=headers, data=payload)
        print(f"GET All Matches: {response.status_code} {response.reason} - {round(time.time()-start, 2)} ms")

        if response.status_code == 200:
            return JsonData(response.json()).GetObjects({ "matches": ["rows"] })["matches"]
        else:
            print(f"ERROR - status code '{response.status_code} {response.reason}' returned from GET All Matches.")


    def _FormatAllMatchesRequest(self):
        return (self._authenticatedUrl + "/_all_docs?include_docs=true", {}, {})
##



## Match Data Formatting
    def FormatMatchData(self, matches:dict):
        columns= [
            "date", "competition", "venue", "keywords",
            "officialRole", "referee", "assistant1", "assistant2", "fourthOfficial", "observer", "fees", "expenses",
            "homeTeam", "homeTeamShort", "homeColor", "awayTeam", "awayTeamShort", "awayColor", 
            "periodsNo", "timings", "extraTimeAvailable", "penaltiesAvailable",
            "misconductcodeId", "sinBinSystem",
            "teamSize", "subsNo", "subOpportunities", "subOpportunitiesCount", "withGoalScorers",
            "matchEvents",
            "matchFinished", "matchAbandoned", "playedExtraTime", "winner",
            "yellowCardHomeTotal", "yellowCardAwayTotal", "redCardHomeTotal", "redCardAwayTotal", "yellowCardPositions", "redCardPositions",
            "goalsHomeTotal", "goalsAwayTotal", "penaltyShotHomeScored", "penaltyShotHomeMissed", "penaltyShotAwayScored", "penaltyShotAwayMissed",
            "minutesPlayed", "injuryTimeByPeriodsTotal", 
            "distanceByPeriodsTotal", "sprintsByPeriodsTotal", "sprintsByPeriodsDistanceTotal", "speedCategoryDurations", "speedCategoryDistances",
            "heartRateAverage", "heartRateMax", "heartRateZoneDuration"
            ]

        matchesDataFrame = pd.DataFrame(columns=columns)
        for match in matches:
            newMatchFrame = self._ExtractMatchData(match["doc"])
            matchesDataFrame = pd.concat([matchesDataFrame, newMatchFrame], ignore_index=True)

        matchesDataFrame = matchesDataFrame.sort_values(by="date").reset_index(drop=True)
        matchesDataFrame.dropna(subset=["date"],inplace=True)

        return matchesDataFrame


    def _ExtractMatchData(self, match:dict):
        newMatchFrame = pd.DataFrame({
            "date": RefSixDateFormatting.GetStringDate(self._GetValue(match, "date"),4),
            "competition": self._GetValue(match, "competition"),
            "venue": self._GetValue(match, "venue"),
            "keywords": self._GetValue(match, "keywords", join=True),
            "officialRole": self._GetValue(match, "officialRole"),
            "referee": self._GetNestedValue(match, "matchOfficials", "referee"),
            "assistant1": self._GetNestedValue(match, "matchOfficials", "assistant1"),
            "assistant2": self._GetNestedValue(match, "matchOfficials", "assistant2"),
            "fourthOfficial": self._GetNestedValue(match, "matchOfficials", "fourthOfficial"),
            "observer": self._GetNestedValue(match, "matchOfficials", "observer"),
            "fees": self._GetNestedValue(match, "earnings", "fees"),
            "expenses": self._GetNestedValue(match, "earnings", "expenses"),
            "homeTeam": self._GetValue(match, "homeTeam"),
            "homeTeamShort": self._GetValue(match, "homeTeamShort"),
            "homeColour": self._GetValue(match, "homeColor"),
            "awayTeam": self._GetValue(match, "awayTeam"),
            "awayTeamShort": self._GetValue(match, "awayTeamShort"),
            "awayColour": self._GetValue(match, "awayColor"),
            "periodsNo": self._GetValue(match, "periodsNo"),
            "timings": self._GetValue(match, "timings"),
            "extraTimeAvailable": self._GetValue(match, "extraTimeAvailable"),
            "penaltiesAvailable": self._GetValue(match, "penaltiesAvailable"),
            "misconductcodeId": self._GetValue(match, "misconductcodeId"),
            "sinBinSystem": self._GetValue(match, "sinBinSystem"),
            "teamSize": self._GetValue(match, "teamSize"),
            "subsNo": self._GetValue(match, "subsNo"),
            "subOpportunities": self._GetValue(match, "subOpportunities"),
            "subOpportunitiesCount": self._GetValue(match, "subOpportunitiesCount"),
            "withGoalScorers": self._GetValue(match, "withGoalScorers"),
            "matchEvents": self._GetValue(match, "matchEvents"),
            "matchFinished": self._GetValue(match, "matchFinished"),
            "matchAbandoned": self._GetValue(match, "matchAbandoned"),
            "playedExtraTime": self._GetValue(match, "playedExtraTime"),
            "winner": None,
            "yellowCardHomeTotal": self._GetNestedValue(match, "stats", "yellowCardHomeTotal"),
            "yellowCardAwayTotal": self._GetNestedValue(match, "stats", "yellowCardAwayTotal"),
            "redCardHomeTotal": self._GetNestedValue(match, "stats", "redCardHomeTotal"),
            "redCardAwayTotal": self._GetNestedValue(match, "stats", "redCardAwayTotal"),
            "yellowCardPositions": self._GetNestedValue(match, "stats", "yellowCardPositions", join=True),
            "redCardPositions": self._GetNestedValue(match, "stats", "redCardPositions", join=True),
            "goalsHomeTotal": self._GetNestedValue(match, "stats", "goalsHomeTotal"),
            "goalsAwayTotal": self._GetNestedValue(match, "stats", "goalsAwayTotal"),
            "penaltyShotHomeScored": self._GetNestedValue(match, "stats", "penaltyShotHomeScored"),
            "penaltyShotHomeMissed": self._GetNestedValue(match, "stats", "penaltyShotHomeMissed"),
            "penaltyShotAwayScored": self._GetNestedValue(match, "stats", "penaltyShotAwayScored"),
            "penaltyShotAwayMissed": self._GetNestedValue(match, "stats", "penaltyShotAwayMissed"),
            "minutesPlayed": self._GetNestedValue(match, "stats", "minutesPlayed"),
            "injuryTimeByPeriodsTotal": None,
            "distanceByPeriodsTotal": None,
            "sprintsByPeriodsTotal": None,
            "sprintsByPeriodsDistanceTotal": None,
            "speedCategoryDurations": self._GetNestedValue(match, "stats", "speedCategoryDurations", join=True),
            "speedCategoryDistances": self._GetNestedValue(match, "stats", "speedCategoryDistances", join=True),
            "heartRateAverage": self._GetNestedValue(match, "stats", "heartRateAverage"),
            "heartRateMax": self._GetNestedValue(match, "stats", "heartRateMax"),
            "heartRateZoneDuration": self._GetNestedValue(match, "stats", "heartRateZoneDuration", join=True)
        }, index=[0])

        return newMatchFrame


    def _GetValue(self, match:dict, column:str, join:bool=False):
        try:
            if join == False:
                return match[column]
            
            string = ""
            for item in match[column]:
                string += str(item) + " "
            return string
        except:
            #print(column)
            return


    def _GetNestedValue(self, match:dict, column1:str, column2:str, join:bool=False):
        try:
            if join == False:
                return match[column1][column2]

            string = ""
            for item in match[column1][column2]:
                string += str(item) + " "
            return string
            
        except:
            #print(column1, column2)
            return
##


###



### JSON File Class - Responsible for handling reading from / writing to JSON files.
class JsonFile:

## Class Setup
    _filePath:str
    _contents:JsonData

    def __init__(self, filePath:str):
        self._ReadFile(filePath)

    def GetContentsObject(self): return self._contents
    def GetData(self): return self._contents.GetData()
    def GetObjects(self, objectPaths:dict): return self._contents.GetObjects(objectPaths)
    def GetAttributeValue(self, attribute:str, objectPath:list): return self._contents.GetObjects({"object": objectPath})["object"][attribute]
##


## Reading JSON Files
    def _ReadFile(self, filePath:str):
        self._filePath = filePath

        try:
            jsonFile = open(self._filePath, "r")
            self._contents = JsonData(json.load(jsonFile))
        except FileNotFoundError:
            print(f"ERROR - contents cannot load. {self._filePath}")
##

###



### JSON Data Class - Responsible for storing JSON data and handling operations on said data.
class JsonData:

## Class Setup
    _data:dict

    def __init__(self, data:dict):
        self._data = data

    def GetData(self): return copy.deepcopy(self._data)
##


## Get JSON Objects
    def GetObjects(self, objectPaths:dict, json:dict=None):
        if json == None: json = self.GetData()

        retrievedObjects = {}

        for objectName in objectPaths:
            jsonCopy = copy.deepcopy(json)
            path = objectPaths[objectName]

            retrievedObjects[objectName] = self._TraverseJson(jsonCopy, path)

        return retrievedObjects


    def _TraverseJson(self, json:dict, objectPath:list):
        nextMove = objectPath[0]
        del objectPath[0]

        try:
            json = json[nextMove]
        except KeyError:
            print(f"ERROR - key not found. {nextMove}")
            return

        if objectPath == []:
            return json

        return self._TraverseJson(json, objectPath)


    def GetObjectsFromArray(self, arrayObjectPath:list, returnObjectsPaths:dict, ignoreMissing:bool = False):
        json = self._TraverseJson(self.GetData(), arrayObjectPath)

        returnObjects = []
        jsonObjects = len(json)

        for i in range(jsonObjects):
            objectData = self.GetObjects(copy.deepcopy(returnObjectsPaths), json[i])

            if (None in objectData.values()) == False:
                returnObjects.append(objectData)

        return returnObjects
##

###



### RefSix Date Formatting - The class responsible for translating the RefSix data format into something usable.
class RefSixDateFormatting:
    @staticmethod
    def GetStringDate(dateString:str, yearLength:int):
        """
        :param string dateString: The RefSix date string.
        :param integer yearLength: The year length, either 2 or 4.

        :return: A string containing the date in YY.MM.DD or YYYY.MM.DD format.
        """

        if dateString == None:
            return

        day = dateString[8:10]
        month = dateString[5:7]
        year = dateString[(4-yearLength):4]

        return f"{year}.{month}.{day}"