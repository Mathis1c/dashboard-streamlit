import streamlit as st
import paho.mqtt.client as mqtt
from queue import Queue
from streamlit_autorefresh import st_autorefresh
import time

st_autorefresh(interval=1000, key="refresh")

BROKER = "4.211.179.237"
PORT = 1883
TOPICS = [
    ("esp/Manu_Auto_mode", 0),
    ("esp/moteur", 0),
    ("esp/servo", 0),
]

# =======================
# RESSOURCE PERSISTANTE
# =======================
@st.cache_resource
def mqtt_resource():
    q = Queue()

    def on_connect(client, userdata, flags, rc):
        print("✅ CONNECT MQTT rc =", rc)
        for topic, _ in TOPICS:
            client.subscribe(topic)
            print("📡 SUB", topic)

    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print("MESSAGE MQTT:", msg.topic, payload)
        q.put((msg.topic, payload))#MISE DANS LA QUEUE
        print("QUEUE SIZE:", q.qsize())

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    return client, q

client, queue = mqtt_resource()

#INIT variables de session
for key in ["motor", "servo", "mode"]:
    if key not in st.session_state:
        st.session_state[key] = "—"




# =======================
# LECTURE QUEUE
# =======================
while not queue.empty():
    topic, payload = queue.get()

    if topic == "esp/moteur":
        st.session_state.motor = payload
    elif topic == "esp/servo":
        st.session_state.servo = payload
    elif topic == "esp/Manu_Auto_mode":
        st.session_state.mode = payload

# =======================
# AFFICHAGE FINAL
# =======================
st.title("Projet Industrie 4.0 système embarque - Dashboard Streamlit")

st.write("⏱ Heure UI :", time.strftime("%H:%M:%S"))
st.write("Moteur :", st.session_state.motor,"______Servo  :", st.session_state.servo,"______Mode   :", st.session_state.mode)


st.write("")
st.write("Mode : manu ou auto") 
mode_choice = st.selectbox("Mode", ["manu", "auto"])
send_topic = "esp/Manu_Auto_mode"
send_payload = False if mode_choice == "auto" else True 
if st.button("changement mode"):
    if send_topic == "esp/Manu_Auto_mode" :
        client.publish(send_topic, str(send_payload))  # envoie True/False
        st.success(f"Message envoyé sur {send_topic}: {send_payload} ({mode_choice})")
        print(f"📤 MESSAGE ENVOYÉ: {send_topic} -> {send_payload} ({mode_choice})")
print("Mode actuel :", st.session_state.mode)
if st.session_state.mode == "True":#manu
    st.write("Mode manuel sélectionné")
    st.subheader("Envoyer un message MQTT")
    

    send_topic = st.selectbox("Topic", ["esp/moteur", "esp/servo"])
    if send_topic == "esp/moteur":
        send_payload = st.number_input("Valeur moteur (0-100)", min_value=0, max_value=100, value=0, step=10)
    elif send_topic == "esp/servo":
        send_payload = st.number_input("Valeur servo (0-90)", min_value=0, max_value=90, value=0, step=10)

    if st.button("Envoyer l'odre manuellement"):
        if send_topic in ["esp/moteur", "esp/servo"]:
            client.publish(send_topic, str(send_payload))
            st.success(f"Message envoyé sur {send_topic}: {send_payload}")
            print(f"📤 MESSAGE ENVOYÉ: {send_topic} -> {send_payload}")
        elif send_topic == "esp/Manu_Auto_mode":
            client.publish(send_topic, str(send_payload))  # envoie True/False
            st.success(f"Message envoyé sur {send_topic}: {send_payload} ({mode_choice})")
            print(f"📤 MESSAGE ENVOYÉ: {send_topic} -> {send_payload} ({mode_choice})")
        else:
            st.warning("⚠️ Entrez un message avant d'envoyer")
elif st.session_state.mode == "False": #auto
    st.write("Mode automatique sélectionné")
    

