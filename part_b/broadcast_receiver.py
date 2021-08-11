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

PORT = 8888

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Reuse previous address, 1 to active, 0 to deactivate
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiver_socket.bind(('', PORT))

while True:
    data, addr = receiver_socket.recvfrom(1024)
    print('Received from {}; Server Time: {}'.format(addr, data.decode()))