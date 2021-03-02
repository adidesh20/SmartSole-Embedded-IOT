from app import app, routes 
import sys
from app.routes import * 
from threading import Thread
import time

def main():
    app.run()



if __name__ == "__main__":
    t1 = Thread (target=process_data, args=())
    t2 = Thread (target=main, args=())
    t3 = Thread (target=data_fixer, args=())
    t1.start()
    t2.start()
    time.sleep(20)
    t3.start()