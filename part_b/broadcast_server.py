#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part B: Develop a broadcast application to disseminate earthquake         #
# and tsunami warning information to all clients on the subnet as follows.  #
# Broadcast server                                                          #
#                                                                           #
#############################################################################

import socket
import time
from datetime import datetime
import re
import json

port = 8888
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


# Custom function to get date with correct format
def custom_get_date():
    errorFlag = True
    inputDate = 0
    while errorFlag:
        try:
            inputDate = str(input("Date of incident occurrence (Format DD/MM/YYYY): "))
            regexCheck = re.match("^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/][0-9]{1,4}\d\d$", inputDate)
            errorFlag = not regexCheck
            print("Incorrect format") if errorFlag else None
        except:
            print("Incorrect format")
    return inputDate


# Custom function to get time with correct format
def custom_get_time():
    errorFlag = True
    inputTime = 0
    while errorFlag:
        try:
            inputTime = str(input("Time of incident occurrence (Format HHMM): "))
            regexCheck = re.match("^([0-1][0-9]|2[0-3])([0-5][0-9])$", inputTime)
            errorFlag = not regexCheck
            print("Incorrect format") if errorFlag else None
        except:
            print("Incorrect format")
    return inputTime


# Custom function to get the incident type 1 or 2
def custom_get_incident_type():
    errorFlag = True
    inputType = 0
    while errorFlag:
        try:
            inputType = str(input("Type of incident [0 - Earthquake warning] [1 - Tsunami warning]: "))
            regexCheck = re.match("^[0-1]$", inputType)
            errorFlag = not regexCheck
            inputType = "Tsunami warning" if int(inputType) == 1 else "Earthquake warning"
            print("Incorrect format") if errorFlag else None
        except:
            print("Incorrect format")
    return inputType

while True:
    inputDate = custom_get_date()
    inputTime = custom_get_time()
    formattedDateTime = inputDate + " " + inputTime + "hour"
    inputIncidentType = custom_get_incident_type()
    inputLocation = str(input("Enter the location of incident: "))
    inputDescription = str(input("Provide some description for the incident: "))

    currentTime = str(datetime.now())

    JSONData = {
        "incidentDatetime": formattedDateTime,
        "incidentType": inputIncidentType,
        "incidentLocation": inputLocation,
        "incidentDescription": inputDescription,
        "incidentGenerated": currentTime
    }

    sender_socket.sendto(json.dumps(JSONData).encode(), ('<broadcast>', port))
    print('[+] Broadcasted data to UDP port {}'.format(port))

    time.sleep(2)