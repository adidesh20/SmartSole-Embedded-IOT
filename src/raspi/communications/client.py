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

def on_message(client, userdata, message):
    """callback for when message is received

    Args:
        client ([type]): client that caused this callback
        userdata ([type]): None
        message ([type]): Obj with members: topic, payload, qos, retain
    """
    print(message.topic, message.payload)


if __name__ == '__main__':
    client = Client()
    client.client.subscribe("test/")
    client.client.message_callback_add('test/', on_message)
    client.client.publish("test/", payload=bytes('hello', 'UTF-8'))
    client.loop_forever()
