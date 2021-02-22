import paho.mqtt.client as mqtt
import ssl
import sys

'''
Usage: 
- create client instance
- connect to broker
- call a loop function to keep connection alive
- subscribe to topic
- publish to broker
- disconnect from broker
'''

class Client():
    def _on_connect(self,client, userdata, flags, rc):
        """ Callback for MQTT connection"""
        print('Client connected')
    def _on_disconnect(self,client, userdata, rc):
        """Callback for MQTT disconnect"""
        print('Client disconnected')

    def __init__(self, broker_addr='localhost', broker_port=8883, ca_cert='./certs/ca.crt', client_cert='./certs/client.crt', client_key='./certs/client.key', tls=True):
        """Opens mqtt connection between client and broker. Sets up TLS if required.

        Args:
            broker_addr (str, optional): Address of MQTT broker (must match name on CA file if using tls). Defaults to 'localhost'.
            broker_port (int, optional): Port used by broker for mqtt connections. Defaults to 8883.
            ca_cert     (str, optional): Path to certificate authority certificate. Defaults to './certs/ca.crt'.
            client_cert (str, optional): Path to client certificate. Defaults to './certs/client.crt'.
            client_key  (str, optional): Path to client private key. Defaults to './certs/client.key'.
            tls     (boolean, optional): Value deciding wether to use TLS or not. Defaults to True.
        """
        self.client = mqtt.Client('client', clean_session=True, protocol=mqtt.MQTTv311, transport='tcp')
        if tls:
            self.client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, tls_version = ssl.PROTOCOL_TLSv1_2)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.will_set('connection_log', bytes('disconnected', 'utf-8'))
        self.client.username_pw_set('client')
        self.client.connect(broker_addr, port=broker_port, keepalive=60, bind_address="")
    
    def subscribe(self, topic: str, callback):
        """Subscribes to a topic

        Args:
            topic           (str): Name of topic to subscribe to.
            callback   (function): Function to call when a new message is received
        """
        self.client.subscribe(topic)
        self.client.message_callback_add(topic, callback)
    
    def loop_forever(self):
        self.client.loop_forever()


client = Client()
client.subscribe('hello', lambda x:x)
client.loop_forever()


# BROKER_ADDR = 'localhost'
# BROKER_PORT = 1883
# CERTIFICATE = './certs/ca.crt'
# CLIENT_CERT = './certs/client.crt'
# CLIENT_KEY = './certs/client.key'
# connected = False

# def on_connect(client, userdata, flags, rc):
#     print('connected')
#     connected = True
# def on_disconnect(client, userdata, rc):
#     print('disconnect')
#     connected = False

# client = mqtt.Client('client1', clean_session=True,protocol=mqtt.MQTTv311, transport='tcp')
# client.tls_set(ca_certs=CERTIFICATE, certfile=CLIENT_CERT, keyfile=CLIENT_KEY, tls_version = ssl.PROTOCOL_TLSv1_2)
# #client.tls_set(ca_certs=CERTIFICATE, tls_version = ssl.PROTOCOL_TLSv1_2)
# #client.tls_insecure_set(True)
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.will_set('connection_log', bytes('disconnected', 'utf-8'))
# client.username_pw_set('client')
# client.connect(BROKER_ADDR, port=BROKER_PORT, keepalive=60, bind_address="")
# client.subscribe('')
# client.loop_forever()
# print('Made it')


# # client_id = sys.argv[1]
# # transport = "tcp" # can be set to "websocket"
# # client = mqtt.Client(client_id=client_id, clean_session=False, userdata=None, transport=transport)


# # use only if using "websocket above"
# # settings for websocket
# # path: mqtt path to use on the broker
# # headers: dictionary specifying list of extra headers to be appended to standard websocket headers
# # ws_set_options(self, path='/mqtt', headers=None)

# # ca_certs = "../cert/ca.crt"
# # client.tls_set(ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
# # client.tls_insecure_set(True)
# # client.connect(BROKER_ADDR, port = BROKER_PORT)