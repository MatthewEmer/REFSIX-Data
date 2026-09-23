from colorama import Fore, Back, Style
import requests
import json

# Testing Code
def PassedTest(test):
    print(f"{Back.GREEN} PASS {Style.RESET_ALL} {test}")
def FailedTest(test, information):
    print(f"{Back.RED} FAIL {Style.RESET_ALL} {test} | {information}")


def RunTest(test, function, parameters):
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
    return RunTest(f"Information file '{file}' exists and can be read.", read_information_file, {"file": file})

def read_information_file(parameters):
    file = parameters["file"]
    try:
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
        return ("Pass", data)
    
    except FileNotFoundError:
        return ("Fail", f"AssertionError: File does not exist (File: '{file}').")
    

def GetInformationFromFile(informationData, api_call, sections, fields):
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