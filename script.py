import paho.mqtt.client as mqtt
client = mqtt.Client()
assert(client.connect("test.mosquitto.org",port=1883) == 0)


client.publish("IC.embedded/Squadron/","hello3")
