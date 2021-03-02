from app import app, routes 
from app.routes import data_dict, data_lock, global_data, global_data_lock, comms, comms_lock
from threading import Thread
import time

def main():
    app.run()

# every 10 minutes, delete any data collected more than 24 hours before
def data_fixer():
    t = time.time() - 86400
    with global_data_lock:
        # delete entries taken more than a day before (86400 = seconds in a day)
        global_data = global_data[global_data['time'] > t]
    time.sleep(600)


if __name__ == "__main__":
    t1 = Thread (target=routes.mock_data, args=())
    t2 = Thread (target=main, args=())
    t3 = Thread (target=data_fixer, args=())
    t1.start()
    t2.start()
    t3.start()