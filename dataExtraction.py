from colorama import Fore, Back, Style
from datetime import datetime
import requests
import json
import math


## REFSIX API Class
class REFSIX_API:
    _apiAuthorisationData = None

    def __init__(self, filePath):
        """
        Initialises an instance of the REFSIX_API class.

        :param string filePath: The file path for the relevant file.
        """

        self._GetAuthorisationDataWithTest(filePath)


    def _OutputCallStatus(self, apiCall, statusCode):
        """
        Takes a given HTTPS status code and outputs a debug message linking it to the given API call.

        :param string apiCall: The API call that has just been made.
        :param integer statusCode: A HTTPS status code, being given by the API call.
        """

        supportedStatusCodes = {200: "Ok", 400: "Bad Request", 401: "Unauthorised", 404: "Not Found"}
        outputMessage = f"{apiCall}:"

        if statusCode >= 200 and statusCode <= 299:
            outputMessage += Fore.GREEN
        elif statusCode >= 400 and statusCode <= 599:
            outputMessage += Fore.RED
        else: # Unsupported Status Codes
            outputMessage += Fore.YELLOW

        print(outputMessage + f"{statusCode} {supportedStatusCodes[statusCode]}\n")


    def _GetAuthorisationDataWithTest(self, filePath):
        """
        Runs a test which takes the given file path, and retrieves the contents, before saving them in _apiAuthorisationData.

        :param string filePath: The file path for the relevant file.
        """

        test = Test("The authorisation information file exists and can be read from.", None, 0, 9, self._get_authorisation_data, filePath)
        (success, response) = test.RunTest()

        if success == True:
            self._apiAuthorisationData = response


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
        :param any responseType: What response you want the class to test (0: value, 1: length).
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
        :param any responseType: What response you want the class to test (0: value, 1: length).
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
""""

#
def Read_Information_File(file):
    
    Takes the 'information.json' file and returns the contents as a dictionary. The file has been deliberately excluded from the repository for security reasons.

    :param string file: The file path for 'information.json'.

    :return: A dictionary containing the JSON data from the file.

    :raises: The test fails if the file cannot be found, or if it cannot be read.
    

    return Run_Test(f"Information file '{file}' exists and can be read.", read_information_file, {"file": file})

def read_information_file(parameters):
    file = parameters["file"]
    try:
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
        return ("Pass", data)
    
    except FileNotFoundError:
        return ("Fail", f"AssertionError: File does not exist.\n- File: '{file}'.")
    except TypeError:
        return ("Fail", f"AssertionError: File cannot be read.\n- File: '{file}'.")
#


#
def Get_Information_From_File(informationData, apiCall, sections, fields):
    
        Takes a dictionary of JSON data and extracts the requested fields and their data.
    
        :param dictionary informationData: The information collected from 'information.json'.
        :param string apiCall: The name of the API call.
        :param array sections: The list of sections that make up informationData.
        :param dictionary fields: The list of fields that need to be extracted, sorted by section.
    
        :return: A dictionary containing the extracted fields and their corresponding data.
    
        :raises: The test fails if a requested field cannot be found.
        
    
    return Run_Test(f"Information can be collected from the file for {apiCall}.", get_information_from_file, (informationData, sections, fields))

def get_information_from_file(parameters):
    informationData = parameters[0]
    sections = parameters[1]
    fields = parameters[2]

    information = {}
    currentField = ""
    currentSection = ""

    try:
        for section in sections:
            currentSection = section
            for field in fields[currentSection]:
                currentField = field
                information[currentField] = informationData[currentSection][currentField]
        return ("Pass", information)
    except (KeyError, TypeError):
        return ("Fail", f"AssertionError: Key does not exist.\n- Section: '{currentSection}', Field: '{currentField}'.")
#


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