#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part A: Develop a Web API using Flask for the staff to maintain           #
# information about transit stations of the MRT Sungai Buloh - Kajang line  #
# Note: localhost:8888                                                      #
#                                                                           #
#############################################################################
import sqlite3
import json
from flask import Flask, jsonify, request, abort
import sys

app = Flask(__name__)

# 1. GET /api/stations
# 2. GET /api/stations/<int:id>
# 3. POST /api/stations
# 4. PUT /api/stations/<int:id>
# 5. DELETE /api/stations/<int:id>


def Get_row_as_dict(row):
    row_dict = {
    'ID': row[0],
    'CODE': row[1],
    'NAME': row[2],
    'TYPE': row[3],
    }
    return row_dict


@app.route('/')
def Index():
    return '<h1>This is the index page for UECS3123 assignment</h1>'


# 1. GET /api/stations
@app.route('/api/stations', methods=['GET'])
def GetAllStations():
    # Adaptive JSON conversion, inspired and modified from https://stackoverflow.com/a/18054751
    try:
        dbConnection = sqlite3.connect('../database/1704367_UECS3123_Assignment_May2021.sqlite')
        dbConnection.row_factory = sqlite3.Row
        cursor = dbConnection.cursor()
        selectAllQuery = '''SELECT * FROM stations ORDER BY ID;'''
        cursor.execute(selectAllQuery)
        allRows = cursor.fetchall()
        dbConnection.close()
        # Loop all rows, convert into dict, and save into a list
        DictList = [dict(row) for row in allRows]
        return jsonify(DictList), 200
    except Exception as err:
        print("Error with database. Error: ", err)
        abort(400)

    # Structured/Defined JSON conversion as taught in lecture
    # db = sqlite3.connect("../database/1704367_UECS3123_Assignment_May2021.sqlite")
    # cursor = db.cursor()
    # cursor.execute('SELECT * FROM stations ORDER BY ID')
    # rows = cursor.fetchall()
    # print(rows)
    # db.close()
    # rows_as_dict = []
    # db.close()
    # for row in rows:
    #     row_as_dict = Get_row_as_dict(row)
    #     rows_as_dict.append(row_as_dict)
    # return jsonify(rows_as_dict), 200


# 2. GET /api/stations/<int:id>
@app.route('/api/stations/<int:id>', methods=['GET'])
def GetStation(id):
    try:
        dbConnection = sqlite3.connect('../database/1704367_UECS3123_Assignment_May2021.sqlite')
        dbConnection.row_factory = sqlite3.Row
        cursor = dbConnection.cursor()
        cursor.execute('SELECT * FROM stations WHERE ID = ?;', (int(id), ))
        rowData = cursor.fetchone()
        dbConnection.close()
        rowDict = dict(rowData)
        return jsonify(rowDict), 200
    except Exception as err:
        print("Error with database. Error: ", err)
        abort(400)


# 3. POST /api/stations
# Insert
@app.route('/api/stations', methods=['POST'])
def InsertNewStation():
    if not request.json:
        abort(404)

    newStation = (
        request.json['CODE'],
        request.json['NAME'],
        request.json['TYPE'],
    )

    try:
        dbConnection = sqlite3.connect('../database/1704367_UECS3123_Assignment_May2021.sqlite')
        dbConnection.row_factory = sqlite3.Row
        cursor = dbConnection.cursor()
        cursor.execute('INSERT INTO stations (CODE, NAME, TYPE) VALUES (?, ?, ?);', newStation)
        stationID = cursor.lastrowid
        dbConnection.commit()
        response = {
            'id': stationID,
            'affected': dbConnection.total_changes,
        }
        dbConnection.close()
        return jsonify(response), 201
    except Exception as err:
        print("Error with database. Error: ", err)
        abort(400)


# 4. PUT /api/stations/<int:id>
# ID must be in both http address and JSON
@app.route('/api/stations/<int:id>', methods=['PUT'])
def UpdateStation(id):
    if not request.json:
        print("REQUEST IS EMPTY")
        abort(400)

    if 'ID' not in request.json:
        print("ID element not in JSON")
        abort(400)

    if int(request.json['ID']) != id:
        print("ID in request body is not same as from link")
        abort(400)

    updateStation = (
        request.json['CODE'],
        request.json['NAME'],
        request.json['TYPE'],
        int(id)
    )

    try:
        dbConnection = sqlite3.connect('../database/1704367_UECS3123_Assignment_May2021.sqlite')
        cursor = dbConnection.cursor()
        cursor.execute('UPDATE stations SET CODE=?,NAME=?,TYPE=? WHERE ID=? ', updateStation)
        dbConnection.commit()
        response = {
            'ID': id,
            'affected': dbConnection.total_changes,
        }
        dbConnection.close()
        return jsonify(response), 200
    except Exception as err:
        print("Error with database. Error: ", err)
        abort(400)


# 5. DELETE /api/stations/<int:id>
@app.route('/api/stations/<int:id>', methods=['DELETE'])
def DeleteStation(id):
    if not request.json:
        abort(400)

    if 'ID' not in request.json:
        abort(400)

    if int(request.json['ID']) != id:
        abort(400)

    try:
        dbConnection = sqlite3.connect('../database/1704367_UECS3123_Assignment_May2021.sqlite')
        cursor = dbConnection.cursor()
        cursor.execute('DELETE FROM stations WHERE ID=? ', (int(id), ))
        dbConnection.commit()
        response = {
            'ID': id,
            'affected': dbConnection.total_changes,
        }
        dbConnection.close()
        return jsonify(response), 200
    except Exception as err:
        print("Error with database. Error: ", err)
        abort(400)


if __name__=='__main__':
        app.run(debug=True, port=8888)