from colorama import Fore, Back, Style
from datetime import datetime
import requests
import json
import math


## REFSIX API Class
class REFSIX_API:
    _apiAuthorisationData = None
    _loggedIn = False

    def __init__(self, filePath):
        """
        Initialises an instance of the REFSIX_API class.

        :param string filePath: The file path for the relevant file.
        """

        self._GetAuthorisationDataWithTest(filePath)

        data = GetDataFromJson(self._apiAuthorisationData, ["hosts;serverHost", "authentication;refsixUsername"])


    def AttemptLoginWithTest(self):
        responseValues = self._RunAPICall("POST Login")

        test = Test("POST Login provides token data that expires in the future.", datetime.now().timestamp(), 0, 2, GetDataFieldFromJsonForTest, [responseValues, "expires"])
        (self._loggedIn, response) = test.RunTest()

        self._apiAuthorisationData["tokenData"] = { "tokenUsername": responseValues["token"], "tokenPassword": responseValues["password"], "expires": responseValues["expires"] }

        print(self._apiAuthorisationData)
        print(self._loggedIn)


    def _RunAPICall(self, apiCall):
        """
        Recieves the request to run an API call and attempts to carry it out.

        :param string apiCall: The name of the API call you want to make.
        """

        callType = None
        url = None
        headers = None
        payload = None
        
        if apiCall == "POST Login":
            return self._CallPOSTLogin()
        if apiCall == "GET All Matches":
            raise NotImplementedError
        if apiCall == "GET Match":
            raise NotImplementedError
        if apiCall == "PUT Match (update)":
            raise NotImplementedError
        if apiCall == "POST Match (create)":
            raise NotImplementedError
        if apiCall == "DELETE Match":
            raise NotImplementedError
        else:
            raise NameError


    def _RunAPICallWithTest(self, callName, callType, url, headers, payload, expectedStatus = 200, dataType = "normal"):
        """
        Runs the API call within a test on the status code vs. the inputted data.

        :param string callName: The name of the API call being made.
        :param string callType: The type of API call being made (GET, POST, PUT, DELETE).
        :param string url: The URL for the API call.
        :param dictionary headers: The information needed to make the call.
        :param string payload: More information needed for the API call.
        :param integer expectedStatus: The expected HTTPS status code returned with the API call.
        :param string dataType: The type of data being fed into the call (normal, boundary, erroneous).

        :return: A tuple containing the HTTPS status code and the API response data.
        """
        
        test = Test(f"{callName} returns a {expectedStatus} status code when given {dataType} inputs.", expectedStatus, 2, 0, self._run_api_call, [callType, url, headers, payload])
        (success, response) = test.RunTest()

        self._OutputCallStatus(callName, response.status_code, response.url)
        return (response.status_code, response.json())


    def _OutputCallStatus(self, apiCall, statusCode, request):
        """
        Takes a given HTTPS status code and outputs a debug message linking it to the given API call.

        :param string apiCall: The API call that has just been made.
        :param integer statusCode: A HTTPS status code, being given by the API call.
        :param string request: The actual request that was made.
        """

        supportedStatusCodes = {200: "Ok", 400: "Bad Request", 401: "Unauthorised", 404: "Not Found"}
        outputMessage = f"{apiCall}:"

        if statusCode >= 200 and statusCode <= 299:
            outputMessage += Fore.GREEN
        elif statusCode >= 400 and statusCode <= 599:
            outputMessage += Fore.RED
        else: # Unsupported Status Codes
            outputMessage += Fore.YELLOW

        print(outputMessage + f" {statusCode} {supportedStatusCodes[statusCode]}{Style.RESET_ALL} - {request}\n")


    def _GetAuthorisationDataWithTest(self, filePath):
        """
        Runs a test which takes the given file path, and retrieves the contents, before saving them in _apiAuthorisationData.

        :param string filePath: The file path for the relevant file.
        """

        test = Test("The authorisation information file exists and can be read from.", None, 0, 9, self._get_authorisation_data, filePath)
        (success, response) = test.RunTest()

        if success == True:
            self._apiAuthorisationData = response


    def _CallPOSTLogin(self):
        """
        Calls a POST Login request from the API.

        :return: A dictionary containing the returned token and password.
        """
        
        inputFields = GetDataFromJson(self._apiAuthorisationData, ["hosts;serverHost", "authentication;authentication_key", "authentication;refsixUsername", "authentication;refsixPassword"])

        url = inputFields["hosts;serverHost"] + "/auth/login"
        payload = json.dumps({"username": inputFields["authentication;refsixUsername"], "password": inputFields["authentication;refsixPassword"]})
        headers = {"Authorisation": f"Basic {inputFields["authentication;authentication_key"]}", "Content-Type": "application/json"}

        (status, response) = self._RunAPICallWithTest("POST Login", "POST", url, headers, payload)

        return GetDataFromJson(response, ["token", "password", "expires"])


    def _run_api_call(self, parameters):
        """
        Actually runs the API call.

        :param string callType: The type of API call being made (GET, POST, PUT, DELETE) [in parameters, index 0].
        :param string url: The URL for the API call [in parameters, index 1].
        :param dictionary headers: The information needed to make the call [in parameters, index 2].
        :param string payload: More information needed for the API call [in parameters, index 3].

        :return: The response object from the request.
        """

        return requests.request(parameters[0], parameters[1], headers=parameters[2], data=parameters[3])

    
    def _get_authorisation_data(self, filePath):
        """
        Takes the given file path, and retrieves the contents, before saving them in _apiAuthorisationData.

        :param string filePath: The file path for the relevant file.

        :return: The data from the file, or None if it fails.
        """

        try:
            file = open(filePath, "r")
        except FileNotFoundError:
            return None

        try:
            return json.load(file)
        except TypeError:
            return None
##



## Testing Class
class Test:
    _success = None
    _test = None
    _TestCondition = None

    _function = None
    _functionParameters = None

    def __init__(self, test, expectedResponse, responseType, responseComparison, function, functionParameters = None):
        """
        Initialises an instance of the Test class. 

        :param string test: The test to be carried out.
        :param any expectedResponse: The expected return value from the function.
        :param any responseType: What response you want the class to test (0: value, 1: length, 2: status).
        :param any responseComparison: How you want the class to test the response (-2: anything less than expected, -1: leq expected, 0: equal to expected, 1: geq expected, 2: anything greater than expected, 9: neq).
        :param Function function: The function to be tested.
        :param (optional) any functionParameters: The parameter(s) to be passed into the function.
        """

        self._test = test
        self._TestCondition = TestCondition(expectedResponse, responseType, responseComparison)
        
        self._function = function
        self._functionParameters = functionParameters


    def _OutputOutcome(self, response):
        """
        Takes the outcome of the test, and outputs a debug message.

        :param string response: The function return values from the test.
        """

        if self._success == True:
            print(f"{Back.GREEN} PASS {Style.RESET_ALL} {self._test}\n")
        else:
            print(f"{Back.RED} FAIL {Style.RESET_ALL} {self._test}\n- Response: {response}, Expected Response: {self._TestCondition.GetExpectedResponse()}\n")


    def RunTest(self):
        """
        Runs the test and outputs the outcome.

        :return: Returns true if the test passes, and false if it doesn't, alongside the response from the function.
        """

        response = None
        if self._functionParameters == None:
            response = self._function()
        else:
            response = self._function(self._functionParameters)

        self._success = self._TestCondition.TestResponse(response)        

        self._OutputOutcome(response)
        return (self._success, response)
##



## Test Condition Class
class TestCondition:
    _expectedResponse = None
    _responseType = None
    _responseComparison = None

    def __init__(self, expectedResponse, responseType, responseComparison):
        """
        Initialises an instance of the Test Condition class.

        :param any expectedResponse: The expected return value from the function.
        :param any responseType: What response you want the class to test (0: value, 1: length, 2: status).
        :param any responseComparison: How you want the class to test the response (-2: anything less than expected, -1: leq expected, 0: equal to expected, 1: geq expected, 2: anything greater than expected, 9: neq).
        """

        self._expectedResponse = expectedResponse
        self._responseType = responseType
        self._responseComparison = responseComparison


    def GetExpectedResponse(self): return self._expectedResponse


    def TestResponse(self, response):
        """
        Tests whether the given response meets the requirements provided.

        :param any response: The response provided by the Test class.

        :return: True if the test passes, and False if the test fails.
        """

        # Formatting the response.
        responseValue = response
        if self._responseType == 1:
            if type(response) == int:
                responseValue = math.ceil(math.log10(response))
            else:
                responseValue = len(response)
        if self._responseType == 2:
            responseValue = response.status_code

        # Evaluating the response.
        match self._responseComparison:
            case -2:
                return self._expectedResponse > responseValue
            case -1:
                return self._expectedResponse >= responseValue
            case 0:
                return self._expectedResponse == responseValue
            case 1:
                return self._expectedResponse <= responseValue
            case 2:
                return self._expectedResponse <= responseValue
            case 9:
                return self._expectedResponse != responseValue
            case _:
                return False
##


## Utility Functions
def GetDataFromJson(json, returnFields):
    """
    Takes the JSON and navigates it to find the given fields, which are then returned.

    :param dictionary json: The JSON data.
    :param array returnFields: The fields to be returned, stored as an array with each item being the navigation to a field, with the path separated by semicolons.

    :return: A dictionary of the return fields and their values.
    """

    retrievedFields = {}
    for field in returnFields:
        retrievedFields[field] = get_data_from_json(json, field)

    return retrievedFields


def GetDataFieldFromJsonForTest(parameters): return GetDataFromJson(parameters[0], [parameters[1]])[parameters[1]]


def get_data_from_json(json, path):
    """
    Recursively navigates through the JSON by breaking down the given path.

    :param dictionary json: The JSON data.
    :param array returnFields: The fields to be returned, stored as an array with each item being the navigation to a field, with the path separated by semicolons.

    :return: The value stored at the given location, or None if there is a KeyError.
    """

    seperatorIndex = path.find(";")

    if seperatorIndex == -1:
        try:
            return json[path]
        except:
            return None

    parent = path[:seperatorIndex]
    path = path[seperatorIndex+1:]

    try:
        return get_data_from_json(json[parent], path)
    except:
        return None
   
##
""""
#
def Run_API_Call(apiCall, apiNickname, url, headers, payload):
    
    Takes the given parameters and API call, and attempts to run it. Then attempts to deal with the resulting response code.

    :param string apiCall: The type of API call being made (GET, POST, PUT, DELETE).
    :param string apiNickname: The nickname of that specific call.
    :param string url: The URL for the API call.
    :param dictionary headers: The information needed to make the call.
    :param string payload: More information needed for the API call.

    :return: A JSON object containing the response from the API call.

    :raises: HTTPS Status code based on the response from the API.
    

    response = requests.request(apiCall, url, headers=headers, data=payload)

    if response.status_code >= 200 and response.status_code <= 299:
        HTTPS_Status_Success(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")
        return response.json()
    
    if response.status_code >= 400 and response.status_code <= 499:
        HTTPS_Status_Error(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")
        return

    HTTPS_Status_Unknown(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")

def get_information(informationData, apiCall, fields):
    
    :param array sections: The list of sections that make up informationData.
    
    sections = ["hosts", "authentication", "tokenData"]

    fieldData = Get_Information_From_File(informationData, apiCall, sections, fields)

    if fieldData == None: # Failed Test.
        HTTPS_Status_Error("400 Bad Request", apiCall)
        return 

    return fieldData
#


#
def API_POST_Login(informationData):
    
    Runs the POST Login API call, and records the tokens returned.
    
    :param dictionary informationData: The information collected from 'information.json'.

    :return: The dictionary informationData with the updated token data added.
    

    fields = {"hosts": ["serverHost"], "authentication": ["authentication_key", "refsixUsername", "refsixPassword"], "tokenData": []}
    fieldData = get_information(informationData, "POST Login", fields)
    if fieldData == None:
        return

    (tokenUsername, tokenPassword, expires) = Run_Test("When given valid login details, the API returns a token username, password, and expiry.", api_post_login, fieldData)

    informationData["tokenData"] = {"tokenUsername": tokenUsername, "tokenPassword": tokenPassword, "expires": expires}
    return informationData

def api_post_login(fieldData):
    url = fieldData["serverHost"] + "/auth/login"
    payload = json.dumps({"username": fieldData["refsixUsername"], "password": fieldData["refsixPassword"]})
    headers = {"Authorisation": f"Basic {fieldData["authentication_key"]}", "Content-Type": "application/json"}

    response = Run_API_Call("POST", "Login", url, headers, payload)

    if (response == None):
        return ("Fail", f"The API call has not returned any values.")
    try:
        tokenUsername = response["token"]
        tokenPassword = response["password"]
        expires = response["expires"]
        return ("Pass", (tokenUsername, tokenPassword, expires))
    except:
        return ("Fail", f"The API call response does not contain either a 'token', 'password', or 'expiry' field.")
#


# 
def API_GET_All_Matches(informationData, sections):
    
    Runs the GET All Matches API call, and returns the resulting JSON.
    
    :param dictionary informationData: The information collected from 'information.json'.
    :param array sections: The list of sections that make up informationData.

    :return: The dictionary rawMatchData with the resulting data.
"""

# Main Code Area
refsixApi = REFSIX_API("information.json")
refsixApi.AttemptLoginWithTest()