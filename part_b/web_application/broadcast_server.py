#############################################################################
#                                                                           #
# Student: Khew Li Tien 1704367                                             #
# UEEN3123: TCP/IP Network Application Development [MAY 2021]               #
# Part B: Develop a broadcast application to disemminate earthquake         #
# and tsunami warning information to all clients on the subnet as follows.  #
# Broadcast server and receiver                                             #
# Note: 1) Server listen at localhost:5000                                  #
#       2) Broadcast server page at 'http://localhost:5000/sender',         #
#       receiver at 'http://localhost:5000/receiver'                        #
# Assumption: 1) No data checking required for form submission              #
#             2) No reading or storing of data is required / stated in      #
#                the question                                               #
#             3) No external framework / library is used for web development#
#                                                                           #
#############################################################################
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '1704367'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/receiver')
def chat():
    return render_template('broadcast_receiver.html')


@app.route('/sender')
def sender():
    return render_template('broadcast_sender.html')


@socketio.on('connect', namespace='/signal')
def handle_connect():
    print('Connected to channel')


@socketio.on('client_connected', namespace='/signal')
def handle_client_connected(json):
    print('Connection Status: {}'.format(json['connected']))


@socketio.on('message_sent', namespace='/signal')
def handle_client_send_chat(json_data):
    incidentTime = json_data['incidentTime']
    incidentType = json_data['incidentType']
    incidentLocation = json_data['incidentLocation']
    incidentDescription = json_data['incidentDescription']

    JSONData = {
        "incidentTime": incidentTime,
        "incidentType": incidentType,
        "incidentLocation": incidentLocation,
        "incidentDescription": incidentDescription,
        "incidentGenerated": str(datetime.now())
    }

    emit('message_broadcast', json.dumps(JSONData), broadcast=True)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    socketio.run(app, port='5000', debug=True)