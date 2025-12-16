import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Car Dashboard",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Forcer thème clair (version compatible Streamlit 1.20+)
st.markdown(
    """
    <style>
    /* Fond de la page */
    .css-18e3th9 {
        background-color: #f0f2f6;
        color: black;
    }
    /* Titre */
    .css-1d391kg {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True

)

st.title("Dashboard voiture 🚗")

# Exemple d'affichage d'une métrique
st.metric("Mode", "MANU")
