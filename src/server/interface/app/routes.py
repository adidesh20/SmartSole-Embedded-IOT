from app import app
from flask import request
from flask import render_template, Response
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from threading import Lock
import json
from communications.client import Client

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
global_data_lock = Lock()
comms_lock = Lock()

global_data = pd.DataFrame(columns = ['time', 'pressure', 'temperature', 'steps'])
comms = Client()

def mock_data():
    while True:
        with data_lock:
            data_dict['steps'] += 1
            data_dict['temperature'].append(10)
            data_dict['pressure'].append(10)
            data_dict['status'] = str(int(data_dict['status']) + 1)
        time.sleep(1)

def on_data(client, userdata, message):
    new_data = json.loads(message.payload)
    t = time.time()
    with global_data_lock:
        global_data.append( message.payload )
    

def process_data():
    with comms_lock:
        comms.client.subscribe('data/')
        comms.client.message_callback_add('data/', on_data)
    comms.client.loop_forever()


@app.route('/calibrate')
def calibrate():
    # send the calibration signal to the pi
    with comms_lock:
        comms.client.publish('calibrate/', payload=bytes("calibrate", 'UTF-8'))
    # reset the collected data
    with global_data_lock:
        global_data = pd.DataFrame(columns = ['time', 'pressure', 'temperature', 'steps'])
    return {}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    """Returns JSON of newest data. Using flaks all you need to do is return a dict and it automatically converts to JSON.

    Returns:
        dict: data to be passed to the web interface (points to plot)
    """
    # with data_lock:
    #     out = data_dict
    # return out
    # p = lambda x, y: {'x': x, 'y': y}
    # data_tmp = {
    #     'temperatures': [{'x': data_dict['tmp']/10, 'y': data_dict['tmp']}],
    #     'pressures': [{'x': data_dict['tmp']/10, 'y': data_dict['tmp']}],
    #     'step_count': data_dict['tmp'],
    #     'avg_pressure': data_dict['tmp'],
    #     'avg_temperature': data_dict['tmp'],
    #     'status': "You have walked too much, you should try to rest for a while. Too much blood is going to your foot"
    # }
    # data_dict['tmp'] += 1
    with global_data_lock:
        if len(global_data) > 
    return data_tmp
