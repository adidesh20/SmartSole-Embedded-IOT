from app import app
from flask import request
from flask import render_template, Response
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import requests
import time

from flask_socketio import SocketIO, send, emit

all_data = pd.DataFrame()



def process_data():
    # fill in here
    # add MQTT receiving data 

    # process data

    # decide what to send to graphs on the web interface

    emit('data_payload', json_for_interface)

@app.route('/calibrate')
def calibrate():
    # send MQTT signal to calibrate
    # receive response and say "Calibrating" or something





@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/suggestions')
def suggestions():
    text = request.args.get('jsdata')

    suggestions_list = []

    if text:
        r = requests.get('http://suggestqueries.google.com/complete/search?output=toolbar&hl=ru&q={}&gl=in'.format(text))

        soup = BeautifulSoup(r.content, 'lxml')

        suggestions = soup.find_all('suggestion')

        for suggestion in suggestions:
            suggestions_list.append(suggestion.attrs['data'])

        #print(suggestions_list)

    return render_template('suggestions.html', suggestions=suggestions_list)

@app.route('/data')
def data():
    """Returns JSON of newest data. Using flaks all you need to do is return a dict and it automatically converts to JSON.

    Returns:
        dict: data to be passed to the web interface (points to plot)
    """
    return {'steps': 1, 'temperature': 10, 'time': 2, 'pressure': 1}