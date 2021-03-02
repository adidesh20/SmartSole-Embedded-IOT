from app import app
from flask import request
from flask import render_template, Response
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from threading import Lock
import json

'''
Data dict:
    Steps: [{ time, amount of steps in last 24 hours }], clear readings after 24 hours
    Temperature: [{time, temperature}] temperature 
    Pressure: [{time, temperature}] temperature 
'''

'''
When processing data:
    Status: 
'''

data_dict = {
    'steps': 0,
    'temperature': [],
    'pressure': [],
    'status': "2",
    'tmp': 0,
}
data_lock = Lock()

def mock_data():
    while True:
        with data_lock:
            data_dict['steps'] += 1
            data_dict['temperature'].append(10)
            data_dict['pressure'].append(10)
            data_dict['status'] = str(int(data_dict['status']) + 1)
        time.sleep(1)

def process_data():
    # fill in here
    # add MQTT receiving data 

    # process data

    # decide what to send to graphs on the web interface
    pass


@app.route('/calibrate')
def calibrate():
    # send MQTT signal to calibrate
    # receive response and say "Calibrating" or something
    pass

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
    # with data_lock:
    #     out = data_dict
    # return out
    p = lambda x, y: {'x': x, 'y': y}
    data_tmp = {
        'temperatures': [{'x': data_dict['tmp']/10, 'y': data_dict['tmp']}],
        'pressures': [{'x': data_dict['tmp']/10, 'y': data_dict['tmp']}],
        'step_count': data_dict['tmp'],
        'avg_pressure': data_dict['tmp'],
        'avg_temperature': data_dict['tmp'],
        'status': "You have walked too much, you should try to rest for a while. Too much blood is going to your foot"
    }
    data_dict['tmp'] += 1
    return data_tmp
