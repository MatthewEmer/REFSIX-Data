from colorama import Fore, Back, Style
from datetime import datetime
import requests
import json

# HTTPS Status Codes
def HTTPS_Status_Success(status, result, information):
    print(f"{Back.LIGHTGREEN_EX} {status} {Style.RESET_ALL} {result} | {information}\n")
def HTTPS_Status_Error(status, result, information):
    print(f"{Back.LIGHTRED_EX} {status} {Style.RESET_ALL} {result} | {information}\n")
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
        return None
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

    :test: Fails if the file cannot be found, or if it cannot be read.
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
    
        :test: Fails if a requested field cannot be found.
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
def Run_API_Call(apiCall, url, headers, payload):
    response = requests.request(apiCall, url, headers=headers, data=payload)

    print(response.status_code)
#


#
def API_POST_Login(informationData, sections):
    """
    
    :param dictionary informationData: The information collected from 'information.json'.
    :param array sections: The list of sections that make up informationData.
    """

    fields = {"hosts": ["serverHost"], "authentication": ["authentication_key", "refsixUsername", "refsixPassword"], "tokenData": []}
    fieldData = Get_Information_From_File(informationData, "POST Login", sections, fields)

    if (fieldData == None): # Failed Test.
        HTTPS_Status_Error("400 Bad Request", "'POST Login' API Call Aborted.", "Data cannot be collected for the request.")
        return None 

    response = api_post_login(fieldData)


def api_post_login(fieldData):
    url = fieldData["serverHost"] + "/auth/login"
    payload = json.dumps({"username": fieldData["refsixUsername"], "password": fieldData["refsixPassword"]})
    headers = {"Authorisation": f"Basic {fieldData["authentication_key"]}", "Content-Type": "application/json"}

    Run_API_Call("POST", url, headers, payload)
#


# Main Code Area

informationData = Read_Information_File("information.json")

sections = ["hosts", "authentication", "tokenData"]
API_POST_Login(informationData, sections)