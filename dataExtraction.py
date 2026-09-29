from refsixApiEndpoint import *

api = RefsixApi("information.json")

api.POST_Login()
rawMatchData = api.GET_AllMatches()
matchData = api.FormatMatchData(rawMatchData)

print(matchData)