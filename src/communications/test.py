import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("connected with code: {}".format(str(rc)))
    # subscribe to $SYS topic tree
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print("{} {}".format(msg.topic, str(msg.payload)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)


# can modify, look at docs
client.loop_forever()