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
from datetime import datetime

port = 8888
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# a) Date & Time of Occurence
# b) Type (Earthquake / Tsunami Warning)
# c) Location
# d) Description
# Continuously check for input while the server is up
while True:
    # response = str(datetime.now())
    inputDate = str(input("Date of incident occurence (Format YYYY/MM/DD): "))
    formattedDate = datetime.strptime(inputDate, "%Y/%m/%d")
    print(formattedDate)

    sender_socket.sendto(formattedDate.encode(), ('<broadcast>', port))
    print('[+]Broadcasted data to UDP port {}'.format(port))

    time.sleep(3)