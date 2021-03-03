from app import app
import sys
from flask import request
from flask import render_template, Response
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

global_data = pd.DataFrame(columns = ['time', 'pressure', 'temperature', 'steps', 'max_pressure'])

fresh_data_lock = Lock()
fresh_data = pd.DataFrame(columns = ['time', 'pressure', 'temperature', 'steps', 'max_pressure'])
comms = Client(sys.argv[1])
total_steps = 0

# every 10 minutes, delete any data collected more than 24 hours before
def data_fixer():
    global global_data_lock
    global global_data
    t = time.time() - 86400
    with global_data_lock:
        # delete entries taken more than a day before (86400 = seconds in a day)
        global_data = global_data[global_data['time'] > t]
    time.sleep(600)


def on_data(client, userdata, message):
    global global_data_lock
    global global_data
    global fresh_data
    global total_steps
    new_data = json.loads(message.payload)
    t = time.time()
    with global_data_lock:
        to_add = pd.DataFrame(new_data).round(2)
        global_data = global_data.append( to_add, ignore_index=True )
        fresh_data = fresh_data.append( to_add, ignore_index=True )
    total_steps = global_data['steps'].sum()
    
    

def process_data():
    global comms_lock
    with comms_lock:
        comms.client.subscribe('data/')
        comms.client.message_callback_add('data/', on_data)
    comms.client.loop_forever()


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
    global fresh_data_lock
    global fresh_data
    global total_steps
    with fresh_data_lock:
        data_tmp = fresh_data.to_dict()
    data_tmp['total_steps'] = total_steps    
    # take averages over past 2 minutes
    df = global_data.tail(4)
    data_tmp['avg_temperature'] = round(df['temperature'].mean(), 2)
    data_tmp['max_pressure_single'] = round(df['max_pressure'].max(), 2)
    fresh_data = pd.DataFrame(columns = ['time', 'pressure', 'temperature', 'steps', 'max_pressure'])
    return data_tmp
