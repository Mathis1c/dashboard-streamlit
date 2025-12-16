import streamlit as st
import paho.mqtt.client as mqtt

# --- Configuration MQTT ---
BROKER = "4.211.179.237"  # Remplace par l'IP de ton Mosquitto
PORT = 1883
TOPICS = [("esp/moteur", 0), ("esp/servo", 0), ("esp/Manu_Auto_mode", 0)]

# --- Variables pour stocker les valeurs ---
if "mode" not in st.session_state:
    st.session_state.mode = "N/A"
if "motor" not in st.session_state:
    st.session_state.motor = "N/A"
if "servo" not in st.session_state:
    st.session_state.servo = "N/A"

# --- Callback quand un message arrive ---
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == "esp/Manu_Auto_mode":
        st.session_state.mode = payload
    elif msg.topic == "esp/moteur":
        st.session_state.motor = payload
    elif msg.topic == "esp/servo":
        st.session_state.servo = payload

# --- Client MQTT ---
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPICS)
client.loop_start()

# --- Affichage Streamlit ---
st.title("Dashboard (MQTT)")
st.write("Mode :", st.session_state.mode)
st.write("Motor :", st.session_state.motor)
st.write("Servo :", st.session_state.servo)
