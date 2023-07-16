from paho.mqtt import client as mqtt_client
import random
import json
import time
import yagmail

# Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "mensaje"
TOPIC_ALERT = "mensaje"
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc))


def on_message(client, userdata, msg):
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
        publish(client, TOPIC_ALERT, )

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

def publish(client, topic, message):
    msg = json.dumps(message)
    result = client.publish(topic, msg)

client = connect_mqtt()

#correo electronico
email = 'quishpebryan10mob@gmail.com'
contraseña = 'oihqcvwoxpaevsbz'






def run():
    counter = 1

    while True:
        client.loop_start()
        time.sleep(1)

        if FLAG_CONNECTED:
            if counter % 10 == 0:
                publish(client, TOPIC_ALERT, counter)
                publish(client, TOPIC_ALERT, "Multiplo de 10: {counter}".format(counter=counter))
                yag = yagmail.SMTP(user=email, password=contraseña)
                destinatarios = ['quishpebryan1234@gmail.com']
                asunto = 'multiplo de 10'
                mensaje = 'El número {counter} es múltiplo de 10'.format(counter=counter)
                yag.send(destinatarios, asunto, mensaje)
            else:
                publish(client, TOPIC_ALERT, counter)
            counter += 1
        else:
            client.loop_stop()

if __name__ == '__main__':
    run()
