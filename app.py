import streamlit as st
import paho.mqtt.client as mqtt
import time

BROKER = "4.211.179.237"
PORT = 1883
TOPICS = [("esp/Manu_Auto_mode",0), ("esp/moteur",0), ("esp/servo",0)]

# Variables session
for var in ["mode","motor","servo"]:
    if var not in st.session_state:
        st.session_state[var] = "N/A"

# Callback MQTT
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == "esp/Manu_Auto_mode":
        st.session_state.mode = payload
    elif msg.topic == "esp/moteur":
        st.session_state.motor = payload
    elif msg.topic == "esp/servo":
        st.session_state.servo = payload

# Client MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPICS)
client.loop_start()

# Zone pour affichage dynamique
placeholder_mode = st.empty()
placeholder_motor = st.empty()
placeholder_servo = st.empty()

st.title("Car Dashboard (MQTT)")

# Boucle de mise à jour
while True:
    placeholder_mode.write(f"Mode : {st.session_state.mode}")
    placeholder_motor.write(f"Motor : {st.session_state.motor}")
    placeholder_servo.write(f"Servo : {st.session_state.servo}")
    time.sleep(1)  # Rafraîchissement toutes les 1s
