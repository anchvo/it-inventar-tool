import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="IT Inventar Tool",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Inventar Tool")

# Session State für Daten
if "inventar" not in st.session_state:
    st.session_state.inventar = []

st.header("Neues Gerät hinzufügen")

with st.form("device_form"):
    geraet = st.text_input("Gerät")
    standort = st.text_input("Standort")
    benutzer = st.text_input("Benutzer")
    status = st.selectbox("Status", ["Aktiv", "Defekt", "Reserve"])

    submitted = st.form_submit_button("Hinzufügen")

    if submitted:
        if geraet:
            st.session_state.inventar.append({
                "Gerät": geraet,
                "Standort": standort,
                "Benutzer": benutzer,
                "Status": status
            })
            st.success("Gerät hinzugefügt!")
        else:
            st.error("Bitte mindestens 'Gerät' ausfüllen")

st.divider()

st.header("Inventar")

if st.session_state.inventar:
    df = pd.DataFrame(st.session_state.inventar)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Noch keine Geräte vorhanden")