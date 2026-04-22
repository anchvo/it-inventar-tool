import streamlit as st
import pandas as pd
import uuid


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
                "id": str(uuid.uuid4()),
                "Gerät": geraet,
                "Standort": standort,
                "Benutzer": benutzer,
                "Status": status
            })
            st.success("Gerät hinzugefügt!")
        else:
            st.error("Bitte mindestens 'Gerät' ausfüllen")

st.divider()

st.header("Suche")

search = st.text_input("Suche nach Gerät, Standort, Benutzer oder Status")

st.header("Inventar")

# Jedes Gerät einzeln in einer Liste um einen Delete Button hinzufügen zu können / Tabellen nicht editierbar in Streamlit
# Stabile ID's mit uuid 
if st.session_state.inventar:

    # Filter anwenden
    if search:
        filtered = [
            item for item in st.session_state.inventar
            if search.lower() in item["Gerät"].lower()
            or search.lower() in item["Standort"].lower()
            or search.lower() in item["Benutzer"].lower()
            or search.lower() in item["Status"].lower()
        ]
    else:
        filtered = st.session_state.inventar

    # Anzeige
    for item in filtered:

        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(
                f"""
                **🖥️ {item['Gerät']}**  
                📍 {item['Standort']}  
                👤 {item['Benutzer']}  
                📊 {item['Status']}
                """
            )

        with col2:
            if st.button("🗑️ Delete", key=item["id"]):
                st.session_state.inventar = [
                    x for x in st.session_state.inventar
                    if x["id"] != item["id"]
                ]
                st.rerun()

else:
    st.info("Noch keine Geräte vorhanden")