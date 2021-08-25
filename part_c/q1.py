#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part C:   Reads data about transit stations from a CSV file and store     #
#           them on the server via the Web API.                             #
# Assumption: 1) Insert without considering ID. Allow duplicates.           #
#                                                                           #
#############################################################################
import http.client
import json
import csv

HOST = 'localhost'
PORT = 8888

print('[!] Connecting to {}:{}'.format(HOST, PORT))
conn = http.client.HTTPConnection(HOST, PORT)


# Custom function to check if CSV has all the required headers
def CheckHeader(file):
    requiredFields = [
        'CODE',
        'NAME',
        'TYPE',
    ]
    headerRow = file.fieldnames
    intersection = set(requiredFields) & set(headerRow)
    return len(intersection) == len(requiredFields)


try:
    print('[!] Reading CSV titled "insert_stations.csv"')
    with open('insert_stations.csv') as file:
        print('[!] Checking CSV fields ...')
        readStations = csv.DictReader(file)
        if CheckHeader(readStations):
            print('[!] CSV field names are correct \n')
            for station in readStations:
                stationDict = dict(station)
                print(stationDict)
                conn.request('POST', '/api/stations', json.dumps(stationDict), {
                 'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 })
                response = conn.getresponse()
                if response.status == 201:
                    print('[+] Insert successful for code: ' + stationDict['CODE'])
                    print('[!] Return message: {}'.format(json.loads(response.read())))
                elif response.status == 400:
                    print('[-] INSERTION FAILED!')
                    print('[!] Return message: {}'.format(json.loads(response.read())))
                else:
                    print('[!] Return message: {}'.format(json.loads(response.read())))
            print("\n[!] Insertion completed")
        else:
            print("\n[!] CSV does not contain all the required fields: 'CODE', 'NAME', 'TYPE'")
except FileNotFoundError:
    print('[!] Failed to open CSV file (perhaps the file is not in the same directory?)')