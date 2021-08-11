#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part B: Develop a broadcast application to disemminate earthquake         #
# and tsunami warning information to all clients on the subnet as follows.  #
# Broadcast receiver                                                        #
#                                                                           #
#############################################################################
import socket
import json

PORT = 8888

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiver_socket.bind(('', PORT))

while True:
    data, addr = receiver_socket.recvfrom(1024)
    data_as_object = json.loads(data.decode())
    data_formatted = json.dumps(data_as_object, indent=2)
    print('Received from {}; Data: {}'.format(addr, data_formatted))