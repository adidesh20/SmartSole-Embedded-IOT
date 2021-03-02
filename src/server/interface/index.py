from app import app, routes 
from app.routes import data_dict, data_lock
from threading import Thread

def main():
    app.run()


if __name__ == "__main__":
    t1 = Thread (target=routes.mock_data, args=())
    t2 = Thread (target=main, args=())
    t1.start()
    t2.start()