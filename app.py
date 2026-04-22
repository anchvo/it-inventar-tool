import streamlit as st
import pandas as pd
import uuid


st.set_page_config(
    page_title="IT Inventar Tool",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Inventar Tool")

# Initialisierung des Speichers / Session State für Daten (init)
if "inventar" not in st.session_state:
    st.session_state.inventar = []

# Bearbeitung von Einträgen
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# Gerät hinzufügen oder bearbeiten
st.header("Neues Gerät hinzufügen / bearbeiten")

# Default-Werte für Edit-Modus
edit_item = None

if st.session_state.edit_mode:
    edit_item = next(
        (item for item in st.session_state.inventar 
         if item["id"] == st.session_state.edit_id),
        None
    )

with st.form("device_form"):
    geraet = st.text_input("Gerät", value=edit_item["Gerät"] if edit_item else "")
    standort = st.text_input("Standort", value=edit_item["Standort"] if edit_item else "")
    benutzer = st.text_input("Benutzer", value=edit_item["Benutzer"] if edit_item else "")
    status = st.selectbox(
        "Status",
        ["Aktiv", "Defekt", "Reserve"],
        index=["Aktiv", "Defekt", "Reserve"].index(edit_item["Status"]) if edit_item else 0
    )

    submitted = st.form_submit_button("Speichern")

    if submitted:
        if geraet:

            if st.session_state.edit_mode:
                # UPDATE
                for item in st.session_state.inventar:
                    if item["id"] == st.session_state.edit_id:
                        item["Gerät"] = geraet
                        item["Standort"] = standort
                        item["Benutzer"] = benutzer
                        item["Status"] = status

                st.success("Gerät aktualisiert!")
                st.session_state.edit_mode = False
                st.session_state.edit_id = None

            else:
                # CREATE
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

# Jedes Gerät einzeln in einer Liste für Delete Button
# / Tabellen nicht editierbar in Streamlit
# Stabile ID's mit uuid statt index keys
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
            # Bearbeiten Button
            if st.button("✏️ Bearbeiten", key=f"edit_{item['id']}"):
                st.session_state.edit_mode = True
                st.session_state.edit_id = item["id"]
                st.rerun()

            # Löschen Button
            if st.button("🗑️ Löschen", key=item["id"]):
                st.session_state.inventar = [
                    x for x in st.session_state.inventar
                    if x["id"] != item["id"]
                ]
                st.rerun()

else:
    st.info("Noch keine Geräte vorhanden")