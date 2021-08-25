#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part C:   A script is required to read the updates from a CSV file and    #
#           perform the updates to the data on the server via the           #
#           Web API.                                                        #
# Note: Update using ID. Update without checking.                           #
# Assumption: 1) Change station name only, retain station CODE and TYPE     #
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
        'ID',
        'NAME',
    ]
    headerRow = file.fieldnames
    intersection = set(requiredFields) & set(headerRow)
    return len(intersection) == len(requiredFields)


try:
    print('[!] Reading CSV titled "update_stations.csv"')
    with open('update_stations.csv') as file:
        print('[!] Checking CSV fields ...')
        readStations = csv.DictReader(file)
        if CheckHeader(readStations):
            print('[!] CSV field names are correct \n')
            for station in readStations:
                CSVStationDict = dict(station)
                print(CSVStationDict)

                # Fetch station data (CODE, TYPE) from server
                conn.request('GET', '/api/stations/'+CSVStationDict['ID'])
                getResponse = conn.getresponse()
                if getResponse.status != 200:
                    print('[!] Error retrieving station data. (Perhaps station with the ID does not exist)')
                    print('[!] Skipping update for current data (ID: {})'.format(CSVStationDict['ID']))
                    continue

                getStation = json.loads(getResponse.read())
                print(getStation)

                putData = {
                    'ID': CSVStationDict['ID'],
                    'CODE': getStation['CODE'],
                    'NAME': CSVStationDict['NAME'],
                    'TYPE': getStation['TYPE'],
                }

                conn.request('PUT', '/api/stations/'+CSVStationDict['ID'], json.dumps(putData), {
                 'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 })
                putResponse = conn.getresponse()
                if putResponse.status == 200:
                    print('[+] Update successful for ID: ' + CSVStationDict['ID'] + ' code: ' + getStation['CODE'])
                    print('[!] Return message: {}'.format(json.loads(putResponse.read())))
                elif putResponse.status == 400:
                    print('[-] UPDATE FAILED!')
                    print('[!] Return message: {}'.format(json.loads(putResponse.read())))
                else:
                    print('[!] Return message: {}'.format(json.loads(putResponse.read())))
            print("\n[!] Update completed")
        else:
            print("\n[!] CSV does not contain all the required fields: 'ID', 'NAME'")
except FileNotFoundError:
    print('[!] Failed to open CSV file (perhaps the file is not in the same directory?)')