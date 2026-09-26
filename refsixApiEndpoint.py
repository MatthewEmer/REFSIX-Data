### Importing Libraries
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

    def __init__(self, filePath:str):
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
        else:
            print(f"ERROR - status code {response.status_code} returned from POST Login.")


    def _FormatLoginRequest(self):
        authenticationData = self._authenticationFile.GetObjects({ "authentication": ["authentication"] })["authentication"]

        url = self._authenticationFile.GetAttributeValue("serverHost", ["hosts"])
        headers = { "Authentication": f"Bearer {authenticationData["authentication_key"]}", "Content-Type": "application/json" }
        payload = json.dumps({ "username": authenticationData["refsixUsername"], "password": authenticationData["refsixPassword"] })

        return (url, headers, payload)
##


## GET All Matches
    def GET_AllMatches(self):
        (url, headers, payload) = self._FormatAllMatchesRequest()

        start = time.time()
        response = self._apiSession.get(url, headers=headers, data=payload)
        print(f"GET All Matches: {response.status_code} {response.reason} - {round(time.time()-start, 2)} ms")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"ERROR - status code {response.status_code} returned from GET All Matches.")


    def _FormatAllMatchesRequest(self):
        return (self._authenticatedUrl + "/_all_docs?include_docs=true", {}, {})
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



### Main Code Area

api = RefsixApi("information.json")

api.POST_Login()

matchData = JsonData(api.GET_AllMatches())

matchSummaries = matchData.GetObjectsFromArray(["rows"], { "Date": ["doc", "date"], "Home Team": ["doc", "homeTeam"], "Away Team": ["doc", "awayTeam"] })

matchDates = []
for match in matchSummaries:
    matchDates.append(match["Date"])

matchSummaries = [val for _, val in sorted(zip(matchDates, matchSummaries))]

for match in matchSummaries:
    print(f"\n{match}")    