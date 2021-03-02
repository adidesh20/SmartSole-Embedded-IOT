import numpy as np
import sys
from communications.client import Client
from sensors.sensors import SensorInterface
from sensors.step import Step
import time
import json

if __name__ == '__main__':
    comms = Client(broker_addr=sys.argv[1])
    comms.client.subscribe('data/')
    sense = SensorInterface()
    step_counter = Step()
    while True:
        step_count = 0
        data = {
            'time': [],
            'pressure': [],
            'temperature': [],
            'steps': [],
            'max_pressure': []
        }

        # every 10 seconds
        for i in range(4):
            pressure = []
            temp = []
            steps = 0
            
            # about 0.5 seconds per iteration. overall 2.5 sec
            for i in range(5):
                readings = sense.read_as_dict()
                pressure.append(readings['manometer'])
                temp.append(readings['thermopile'])
                steps += step_counter.is_step( readings['accelerometer'] ) 
                
            data['time'].append(time.time())
            data['pressure'].append( np.mean(pressure) )
            data['temperature'].append( np.mean(temp) )
            data['steps'].append( steps )
            data['max_pressure'].append( np.amax(pressure) )

        comms.client.publish('data/', json.dumps(data))
