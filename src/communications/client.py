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
BRKOER_ADDR = '?.ee.ic.ac.uk'
BROKER_PORT = 8080
client_id = sys.argv[1]
transport = "tcp" # can be set to "websocket"
client = mqtt.Client(client_id=client_id, clean_session=False, userdata=None, transport=transport)


# use only if using "websocket above"
# settings for websocket
# path: mqtt path to use on the broker
# headers: dictionary specifying list of extra headers to be appended to standard websocket headers
# ws_set_options(self, path='/mqtt', headers=None)

ca_certs = "../cert/ca.crt"
client.tls_set(ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.connect(BROKER_ADDR, port = BROKER_PORT)