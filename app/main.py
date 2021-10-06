#right now only a simple hull to be able to use sockets to communicate with a server


from flask import Flask, render_template, request
import json
import pandas as pd
import numpy as np
import string
#from query import QueryControler
import query
import logging
from logging.handlers import RotatingFileHandler


formatter = logging.Formatter("[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s")
handler = RotatingFileHandler('log/main.log', maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(handler)

app = Flask(__name__)

log.info("Entering app")

file_one=pd.read_csv("data.csv")

list_datasets=file_one.title
log.info("file loaded")
queryObj=query.QueryControler(file_one)
log.info("querycontroler loaded")


log.info("loading finished")
@app.route('/querulant', methods=['post','get'])

def sessions():
    message = ''
    log.info("entering a session")
    languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
    if request.method == 'POST':
        nachricht = request.form.get('nachricht')  # access the data inside 
        log.info("NACHRICHT:"+nachricht)
        ogd_check = request.form.get('ogd_check')
        result=queryObj.lookup_query(nachricht,ogd_check)
        print(result)
        message=result

    return render_template('session.html',message=message,languages=list_datasets)



