#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part C:   Downloads data about all transit stations from the server via   #
#           the Web API and saves them in a CSV file.                       #
#                                                                           #
#############################################################################
import http.client
import json
import csv

HOST = 'localhost'
PORT = 8888

print('[!] Connecting to {}:{}'.format(HOST, PORT))
conn = http.client.HTTPConnection(HOST, PORT)
print('[!] Sending HTTP Request')
conn.request('GET', '/api/stations')

response = conn.getresponse()
print('[!] HTTP Response Received')


if response.status == 200:
    stations = json.loads(response.read())
    print('[!] Writing CSV File')

    with open('read_stations.csv', 'w', newline='') as file:
        fields = [
        'ID',
        'CODE',
        'NAME',
        'TYPE',
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for station in stations:
            writer.writerow(station)
        print('[!] Writing completed! CSV saved as "read_stations.csv"!')

else:
    print('[!] ERROR: {}'.format(response.status))