from paho.mqtt import client as mqtt_client
import random
import json
import time
import yagmail
import psutil

# Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "mensajeq"
TOPIC_ALERT = "mensajeq"
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

# correo electrónico
email = 'quishpebryan10mob@gmail.com'
contraseña = 'oihqcvwoxpaevsbz'

def run():
  

    while True:
        client.loop_start()
        time.sleep(2)

        if FLAG_CONNECTED:
                cpu_usage = psutil.cpu_percent()
                publish(client, TOPIC_ALERT, "{cpu_usage}%".format(cpu_usage=cpu_usage))

                if cpu_usage >= 40:
                    yag = yagmail.SMTP(user=email, password=contraseña)
                    destinatarios = ['baquishpet@uce.edu.ec']
                    asunto = 'Uso de CPU elevado'
                    mensaje = 'El porcentaje de uso de la CPU es {cpu_usage}%'.format(cpu_usage=cpu_usage)
                    yag.send(destinatarios, asunto, mensaje)
                else:
                     publish(client, TOPIC_ALERT, "{cpu_usage}%, sin novedades".format(cpu_usage=cpu_usage))

                  

        else:
            client.loop_stop()
if __name__ == '__main__':
      run()
