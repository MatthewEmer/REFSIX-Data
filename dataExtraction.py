from colorama import Fore, Back, Style
import requests
import json

def PassedTest(test):
    print(f"{Back.GREEN} PASS {Style.RESET_ALL} {test}")
def FailedTest(test, information):
    print(f"{Back.RED} FAIL {Style.RESET_ALL} {test} | {information}")

def ReadInformationFile():
    test = "File 'information.json' can be read."
    try:
        with open("information.json", "r") as file:
            data = json.load(file)
        PassedTest(test)
        return data
    except FileNotFoundError:
        FailedTest(test, "AssertionError: File 'information.json' does not exist.")
    except:
            FailedTest(test, "AssertionError: File cannot be read.")


informationData = ReadInformationFile()