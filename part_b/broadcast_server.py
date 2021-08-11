#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part B: Develop a broadcast application to disemminate earthquake         #
# and tsunami warning information to all clients on the subnet as follows.  #
# Broadcast server                                                          #
#                                                                           #
#############################################################################

import socket
import time
import re

port = 8888
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# a) Date & Time of Occurrence
# b) Type (Earthquake / Tsunami Warning)
# c) Location
# d) Description
# Continuously check for input while the server is up

def customGetDate():
    errorFlag = True
    inputDate = 0
    while errorFlag:
        try:
            inputDate = str(input("Date of incident occurrence (Format DD/MM/YYYY): "))
            regexCheck = re.match("^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/][0-9]{1,4}\d\d$", inputDate)
            errorFlag = not regexCheck
        except:
            print("Incorrect format")
    return inputDate

def customGetTime():
    errorFlag = True
    inputTime = 0
    while errorFlag:
        try:
            inputTime = str(input("Time of incident occurrence (Format HHMM): "))
            regexCheck = re.match("^([0-1][0-9]|2[0-3])([0-5][0-9])$", inputTime)
            errorFlag = not regexCheck
        except:
            print("Incorrect format")
    return inputTime

while True:
    # response = str(datetime.now())
    inputDate = customGetDate()
    print(inputDate)
    # [-] No need to convert input date to datetime object
    # formattedDate = datetime.strptime(inputDate, "%d/%m/%Y")
    inputTime = customGetTime()
    print(inputTime)

    sender_socket.sendto(inputDate.encode(), ('<broadcast>', port))
    print('[+]Broadcasted data to UDP port {}'.format(port))

    time.sleep(3)