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
BROKER_ADDR = 'localhost'
BROKER_PORT = 1883
CERTIFICATE = './certs/ca.crt'
CLIENT_CERT = './certs/client.crt'
CLIENT_KEY = './certs/client.key'
connected = False

def on_connect(client, userdata, flags, rc):
    print('connected')
    connected = True
def on_disconnect(client, userdata, rc):
    print('disconnect')
    connected = False

client = mqtt.Client('client1', clean_session=True,protocol=mqtt.MQTTv311, transport='tcp')
client.tls_set(ca_certs=CERTIFICATE, certfile=CLIENT_CERT, keyfile=CLIENT_KEY, tls_version = ssl.PROTOCOL_TLSv1_2)
#client.tls_set(ca_certs=CERTIFICATE, tls_version = ssl.PROTOCOL_TLSv1_2)
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.will_set('bread', 0x44)
client.username_pw_set('client2')
client.connect(BROKER_ADDR, port=BROKER_PORT, keepalive=60, bind_address="")
client.subscribe('bread')
client.loop_forever()
print('Made it')


# client_id = sys.argv[1]
# transport = "tcp" # can be set to "websocket"
# client = mqtt.Client(client_id=client_id, clean_session=False, userdata=None, transport=transport)


# use only if using "websocket above"
# settings for websocket
# path: mqtt path to use on the broker
# headers: dictionary specifying list of extra headers to be appended to standard websocket headers
# ws_set_options(self, path='/mqtt', headers=None)

# ca_certs = "../cert/ca.crt"
# client.tls_set(ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_insecure_set(True)
# client.connect(BROKER_ADDR, port = BROKER_PORT)