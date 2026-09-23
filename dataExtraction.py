from colorama import Fore, Back, Style
from datetime import datetime
import requests
import json


# HTTPS Status Codes
def HTTPS_Status_Success(status, call):
    print(f"{call}:{Fore.GREEN} {status}{Style.RESET_ALL}\n")
def HTTPS_Status_Error(status, call):
    print(f"{call}:{Fore.RED} {status}{Style.RESET_ALL}\n")
def HTTPS_Status_Unknown(status, call):
    print(f"{call}:{Fore.YELLOW} {status}{Style.RESET_ALL}\n")
#


# Testing Code
def Passed_Test(test):
    print(f"{Back.GREEN} PASS {Style.RESET_ALL} {test}\n")
def Failed_Test(test, information):
    print(f"{Back.RED} FAIL {Style.RESET_ALL} {test} | {information}\n")


def Run_Test(test, function, parameters):
    """
    Takes a given function, parameters, and test, and checks whether it works correctly or not.

    :param string test: The description of the test.
    :param function function: The function to be tested.
    :param array parameters: An array containing the parameters for the function.

    :return: The return values from the function on a success, or None if the test fails.
    """
    
    responseData = function(parameters)
    testStatus = responseData[0]
    returnedValues = responseData[1]

    if testStatus == "Fail":
        Failed_Test(test, returnedValues)
        return
    else:
        Passed_Test(test)
        return returnedValues
#


#
def Read_Information_File(file):
    """
    Takes the 'information.json' file and returns the contents as a dictionary. The file has been deliberately excluded from the repository for security reasons.

    :param string file: The file path for 'information.json'.

    :return: A dictionary containing the JSON data from the file.

    :raises: The test fails if the file cannot be found, or if it cannot be read.
    """

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
    """
        Takes a dictionary of JSON data and extracts the requested fields and their data.
    
        :param dictionary informationData: The information collected from 'information.json'.
        :param string apiCall: The name of the API call.
        :param array sections: The list of sections that make up informationData.
        :param dictionary fields: The list of fields that need to be extracted, sorted by section.
    
        :return: A dictionary containing the extracted fields and their corresponding data.
    
        :raises: The test fails if a requested field cannot be found.
        """
    
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
    """
    Takes the given parameters and API call, and attempts to run it. Then attempts to deal with the resulting response code.

    :param string apiCall: The type of API call being made (GET, POST, PUT, DELETE).
    :param string apiNickname: The nickname of that specific call.
    :param string url: The URL for the API call.
    :param dictionary headers: The information needed to make the call.
    :param string payload: More information needed for the API call.

    :return: A JSON object containing the response from the API call.

    :raises: HTTPS Status code based on the response from the API.
    """

    response = requests.request(apiCall, url, headers=headers, data=payload)

    if response.status_code >= 200 and response.status_code <= 299:
        HTTPS_Status_Success(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")
        return response.json()
    
    if response.status_code >= 400 and response.status_code <= 499:
        HTTPS_Status_Error(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")
        return

    HTTPS_Status_Unknown(f"{response.status_code} {response.reason}", f"{apiCall} {apiNickname}")  
#


#
def API_POST_Login(informationData, sections):
    """
    Runs the POST Login API call, and records the tokens returned.
    
    :param dictionary informationData: The information collected from 'information.json'.
    :param array sections: The list of sections that make up informationData.

    :return: The dictionary informationData with the updated token data added.
    """

    fields = {"hosts": ["serverHost"], "authentication": ["authentication_key", "refsixUsername", "refsixPassword"], "tokenData": []}
    fieldData = Get_Information_From_File(informationData, "POST Login", sections, fields)

    if fieldData == None: # Failed Test.
        HTTPS_Status_Error("400 Bad Request", "POST Login")
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


# Main Code Area
informationData = Read_Information_File("information.json")

sections = ["hosts", "authentication", "tokenData"]
informationData = API_POST_Login(informationData, sections)

print(informationData["tokenData"])
print(datetime.now().timestamp())