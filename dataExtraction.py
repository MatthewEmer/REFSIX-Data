### Importing Libraries
from colorama import Fore, Back, Style # Coloured text
from datetime import datetime
import requests
import json
import math
### 



## REFSIX API Class
class REFSIX_API:
    """
    The class responsible for handling all interactions between the codebase and REFSIX's API.

    Attributes
    ---
    _apiAuthorisationData : dict (private)
        The private data required to authenticate the connection between the codebase and the API.
    _expiryTime : int (private)
        The integer timestamp when the login token data will expire.
    """

# Class Setup
    _apiAuthorisationData:dict = None
    _expiryTime:int = None

    def __init__(self, filePath:str):
        """
        A public function which initialises an instance of the REFSIX_API class.

        Parameters
        ---
        filePath : string 
            The file path for the file containing the private authentication data.
        """

        self._GetAuthorisationDataWithTest(filePath)


    def _GetAuthorisationDataWithTest(self, filePath:str):
        """
        A private function which runs a test which takes the given file path, and retrieves the contents, before saving them in _apiAuthorisationData.

        Parameters
        ---
        filePath : string
            The file path for the relevant file.
        """

        testCondition = TestCondition(None, 0, 9)
        test = Test("The authorisation information file exists and can be read from.", testCondition, self._ReadAuthorisationDataFile, filePath)
        
        self._apiAuthorisationData = test.RunTest()


    def _ReadAuthorisationDataFile(self, filePath:str):
        """
        A private function which takes the given file path, and retrieves the contents before saving them in _apiAuthorisationData.

        Parameters
        ---
        filePath : string 
            The file path for the relevant file.

        Returns
        ---
            The data from the file, or None if it fails.
        """

        try:
            file = open(filePath, "r")
        except FileNotFoundError:
            return None

        try:
            return dict(json.load(file))
        except TypeError:
            return None
#

# All Calls
    def _RunAPICallWithTest(self, apiRequest:Request, expectedStatus:int = 200, dataType:str = "normal"):
        """
        A private function which runs a test on the status code retrieved from a given API call. It then returns both the status code and the response.

        Parameters
        ---
        apiRequest : Request 
            The API request to be run.
        expectedStatus : integer (optional)
            The expected HTTPS status code returned with the API call. [Default = 200]
        dataType : string (optional)
            The type of data being fed into the call (normal, boundary, erroneous). [Default = "normal"]
        """

        testCondition = TestCondition(expectedStatus, 0, 0)
        test = Test(f"{apiRequest.GetName()} returns a {expectedStatus} status code when given {dataType} inputs.", testCondition, apiRequest.RunCall)
        test.RunTest()


    def _CheckExpiredTokens(self):
        """
        A private function which checks whether the authentication tokens are still valid.

        Returns
        ---
            A boolean value, true if the tokens have expired, and false if not.
        """
        return self._expiryTime == None or self._expiryTime <= datetime.now().timestamp()
#

# POST Login
    def AttemptLoginWithTest(self):
        """
        A public function which attempts to format and then make a API POST request to the authentication server to get up-to-date token data.
        """

        if self._apiAuthorisationData == None:
            return
        
        responseValues = self._CallPOSTLogin()

        testCondition = TestCondition(datetime.now().timestamp(), 0, 2)
        test = Test("POST Login provides token data that expires in the future.", testCondition, GetDataFieldFromJsonForTest, [responseValues, "expires"])
        self._expiryTime = test.RunTest()

        if test.GetResult():
            self._apiAuthorisationData["tokenData"] = { "tokenUsername": responseValues["token"], "tokenPassword": responseValues["password"], "expires": responseValues["expires"] }


    def _CallPOSTLogin(self):
        """
        A private funciton which calls a POST Login request from the API.

        Returns
        ---
            A dictionary containing the returned token and password.
        """

        postRequest = self._FormatPOSTLoginRequest()
        self._RunAPICallWithTest(postRequest)
        return GetDataFromJson(postRequest.GetResponseJson(), ["token", "password", "expires"])


    def _FormatPOSTLoginRequest(self):
        """
        A private function which formats all the elements required to make a POST Login request.
        
        Returns
        ---
            A Request object containing the POST Login request.
        """

        inputFields = GetDataFromJson(self._apiAuthorisationData, ["hosts;serverHost", "authentication;authentication_key", "authentication;refsixUsername", "authentication;refsixPassword"])
                
        url = inputFields["hosts;serverHost"] + "/auth/login"
        headers = {"Authorisation": f"Basic {inputFields["authentication;authentication_key"]}", "Content-Type": "application/json"}
        payload = json.dumps({"username": inputFields["authentication;refsixUsername"], "password": inputFields["authentication;refsixPassword"]})
        
        return Request(0, url, headers, payload)
#

##


## Request Class
class Request:
    """
    The class responsible for holding request data and actually making API calls.

    Attributes
    ---
    _nickname : string (private)
        The name of the API call, including the call type.
    _type : string (private)
        The type of request.
    _url : string (private)
        The url for the request.
    _headers : dict (private)
        A dictionary containing the headers for the request.
    _payload : string (private)
        The payload for the request.
    _response : requests.Response (private)
        The response recieved after running the request.
    """

# Class Setup
    _nickname:str = None
    _type:str = None

    _url:str = None
    _headers:dict = None
    _payload:str = None

    _response:requests.Response = None

    def GetName(self): return self._nickname
    def GetStatusCode(self): return self._response.status_code
    def GetResponseJson(self): return dict(self._response.json())


    def __init__(self, call:int, url:str, headers:dict, payload:str):
        """
        A public method which initialises an instance of the Request class.

        Parameters
        ---
        call : int
            The call being made (0: POST Login... to be implemented.)
        url : str
            The URL of the request being made.
        headers : dict 
            The headers required for the request
        payload : str
            The payload required to make the request.
        """

        if call == 0:
            self._nickname = "POST Login"
            self._type = "POST"
        else:
            return

        self._url = url
        self._headers = headers
        self._payload = payload
#

# Running Requests
    def RunCall(self):
        """
        A public method that actually runs the API call and outputs the resulting status code.

        Returns
        ---
            The status code of the operation.
        """

        self._response = requests.request(self._type, self._url, headers=self._headers, data=self._payload)
        self._OutputCallStatus()

        return self.GetStatusCode()


    def _OutputCallStatus(self):
        """
        A private method which outputs a message based on the HTTPS status code recieved from the call's response.
        """
        
        supportedStatusCodes = {200: "Ok", 400: "Bad Request", 401: "Unauthorised", 404: "Not Found"}
        outputMessage = f"{self._nickname}:"

        if self._response.status_code >= 200 and self._response.status_code <= 299:
            outputMessage += Fore.GREEN
        elif self._response.status_code >= 400 and self._response.status_code <= 599:
            outputMessage += Fore.RED
        else: # Unsupported Status Codes
            outputMessage += Fore.YELLOW

        print(f"{outputMessage} {self._response.status_code} {supportedStatusCodes[self._response.status_code]}{Style.RESET_ALL} - {self._url}\n")
#

##



## Testing Class
class Test:
    """
    The class responsible for running tests.

    Attributes
    ---
    _success : bool (private)
        Whether the test succeeded or not.
    _test : string (private)
        The text explanation of the test.
    _testCondition : TestCondition (private)
        The TestCondition object that determines the test's outcome.
    _function : function (private)
        The function being tested.
    _functionParameters : any (private)
        The parameters to be passed into the function.
    """

# Class Setup
    _success:bool = None
    _test:str = None
    _testCondition:TestCondition = None

    _function:function = None
    _functionParameters = None

    def __init__(self, test, testCondition, function, functionParameters = None):
        """
        Initialises an instance of the Test class. 

        Parameters
        ---
        test : string
            The description of the test being carried out.
        testCondition : TestCondition 
            The TestCondition object that determines the test's outcome.
        function : Function 
            The function being tested.
        functionParameters : any (optional)
            The parameters to be passed into the function. [Default = None]
        """

        self._test = test
        self._testCondition = testCondition
        
        self._function = function
        self._functionParameters = functionParameters


    def GetResult(self): return self._success
#

# Running The Test
    def RunTest(self):
        """
        A public function which runs the test and outputs the outcome.

        Returns
        ---
            The return value from the function being tested (if the test succeeds).
        """

        if self._functionParameters == None:
            returnValue = self._function()
        else:
            returnValue = self._function(self._functionParameters)

        self._success = self._testCondition.TestResponse(returnValue)        
        self._OutputOutcome(returnValue)

        if self._success:
            return returnValue


    def _OutputOutcome(self, returnValue):
        """
        A private function which takes the outcome of the test, and outputs a debug message.

        Parameters
        ---
        returnValue : string
            The return value from the tested function.
        """

        outcomeBanner = { True: f"{Back.GREEN} PASS {Style.RESET_ALL}", False: f"{Back.RED} FAIL {Style.RESET_ALL}" }
        comparisonText = { -2: "Must be less than the expected value.", -1: "Must be less than or equal to the expected value.", 0: "Must be equal to the expected value.", 1: "Must be greater than or equal to the expected value.", 2: "Must be greater than the expected value.", 9: "Must not be equal to the expected value." }

        if self._success == True:
            print(f"{outcomeBanner[self._success]} {self._test}\n")
        else:
            print(f"{outcomeBanner[self._success]} {self._test}\n- {comparisonText[self._testCondition.GetComparisonType()]}\n- Expected Response: {self._testCondition.GetExpectedResponse()}, Actual Response: {returnValue}\n")
#

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
    def GetComparisonType(self): return self._responseComparison


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



## Main Code Area
refsixApi = REFSIX_API("information.json")
refsixApi.AttemptLoginWithTest()