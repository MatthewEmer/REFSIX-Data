from colorama import Fore, Back, Style
import requests
import json

# Testing Code
def PassedTest(test):
    print(f"{Back.GREEN} PASS {Style.RESET_ALL} {test}")
def FailedTest(test, information):
    print(f"{Back.RED} FAIL {Style.RESET_ALL} {test} | {information}")


def RunTest(test, function, parameters):
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
        FailedTest(test, returnedValues)
        return None
    else:
        PassedTest(test)
        return returnedValues
#


def ReadInformationFile(file):
    """
    Takes the 'information.json' file and returns the contents as a dictionary. The file has been deliberately excluded from the repository for security reasons.

    :param string file: The file path for 'information.json'.

    :return: A dictionary containing the JSON data from the file.

    :test: Fails if the file cannot be found, or if it cannot be read.
    """

    return RunTest(f"Information file '{file}' exists and can be read.", read_information_file, {"file": file})

def read_information_file(parameters):
    file = parameters["file"]
    try:
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
        return ("Pass", data)
    
    except FileNotFoundError:
        return ("Fail", f"AssertionError: File does not exist (File: '{file}').")
    except TypeError:
        return ("Fail", f"AssertionError: File cannot be read (File: '{file}').")
    

def GetInformationFromFile(informationData, api_call, sections, fields):
    """
        Takes a dictionary of JSON data and extracts the requested fields and their data.
    
        :param dictionary informationData: The information collected from 'information.json'.
        :param string api_call: The name of the API call.
        :param array sections: The list of sections that make up informationData.
        :param dictionary fields: The list of fields that need to be extracted, sorted by section.
    
        :return: A dictionary containing the extracted fields and their corresponding data.
    
        :test: Fails if a requested field cannot be found.
        """
    
    return RunTest(f"Information can be collected from the file for {api_call}.", get_information_from_file, (informationData, sections, fields))

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
        return ("Fail", f"AssertionError: Key does not exist (Section: '{currentSection}' Field: '{currentField}').")


sections = ["hosts", "authentication", "tokenData"]
fields = dict.fromkeys(sections, [])

informationData = ReadInformationFile("information.json")

fields["hosts"] = ["serverHost"]
fields["authentication"] = ["refsixUsername", "refsixPassword"]
data = GetInformationFromFile(informationData, "POST Login", sections, fields)

print(data)