#right now only a simple hull to be able to use sockets to communicate with a server


from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import pandas as pd
import numpy as np
import string
from query import QueryControler

app = Flask(__name__)
socketio = SocketIO(app)

file_one=pd.read_csv("data.csv")

list_datasets=file_one.title

queryObj=QueryControler(file_one)

@app.route('/')
def sessions():
    languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
    return render_template('session.html',languages=list_datasets)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json_msg, methods=['GET', 'POST']):
    print('received my event: ' + str(json_msg))
    if "message" in json_msg:
        print(json_msg["message"])
        #if json_msg["message"] in list_datasets:
        #    print("The word is in the list!")
        #else:
        #    print("The word is not in the list!")
        result=queryObj.lookup_query(json_msg["message"])
        print(result)
    socketio.emit('my response', result, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
