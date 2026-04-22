import streamlit as st
import uuid


st.set_page_config(
    page_title="IT Inventar Tool",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Inventar Tool")

# Initialisierung der Nachrichten
if "message" not in st.session_state:
    st.session_state.message = None

# Initialisierung des Speichers / Session State für Daten (init)
if "inventar" not in st.session_state:
    st.session_state.inventar = []

# Initialisierung des Bearbeitungsmodus
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# Initialisierung für Leeren des Formulars
if "form_counter" not in st.session_state:
    st.session_state.form_counter = 0

# Anzeigen von Nachrichten
if st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = None

# Anzeigetext für Gerät hinzufügen oder bearbeiten
st.header("Neues Gerät hinzufügen / bearbeiten")

# Default-Werte für Edit-Modus
edit_item = None

if st.session_state.edit_mode and st.session_state.edit_id:
    edit_item = next(
        (item for item in st.session_state.inventar 
         if item["id"] == st.session_state.edit_id),
        None
    )

# Default-Werte für Create-Modus
# with st.form(key=f"device_form_{st.session_state.edit_mode}_{st.session_state.edit_id}"):
with st.form(key=f"device_form_{st.session_state.form_counter}"):
    default_geraet = ""
    default_standort = ""
    default_benutzer = ""
    default_status = "Aktiv"

    if st.session_state.edit_mode and edit_item:
        default_geraet = edit_item["Gerät"]
        default_standort = edit_item["Standort"]
        default_benutzer = edit_item["Benutzer"]
        default_status = edit_item["Status"]

    geraet = st.text_input(
        "Gerät",
        value=default_geraet,
    )

    standort = st.text_input(
        "Standort",
        value=default_standort,
    )

    benutzer = st.text_input(
        "Benutzer",
        value=default_benutzer,
    )

    status = st.selectbox(
        "Status",
        ["Aktiv", "Defekt", "Reserve"],
        index=["Aktiv", "Defekt", "Reserve"].index(default_status),
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

                st.session_state.message = "✏️ Gerät aktualisiert!"

                st.session_state.edit_mode = False
                st.session_state.edit_id = None

                st.session_state.form_counter += 1
                st.rerun()

            else:
                # CREATE
                st.session_state.inventar.append({
                    "id": str(uuid.uuid4()),
                    "Gerät": geraet,
                    "Standort": standort,
                    "Benutzer": benutzer,
                    "Status": status
                })

                st.session_state.message = "✅ Gerät hinzugefügt!"

                st.session_state.form_counter += 1
                st.rerun()
   
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

    # Suchfilter anwenden
    filtered = st.session_state.inventar

    if search:
        filtered = [
            item for item in filtered
            if search.lower() in item["Gerät"].lower()
            or search.lower() in item["Standort"].lower()
            or search.lower() in item["Benutzer"].lower()
            or search.lower() in item["Status"].lower()
        ]

    # Anzeige
    for item in filtered:

        col1, col2 = st.columns([5, 1])

        with col1:
            c1, c2, c3, c4 = st.columns(4)

            c1.write(f"🖥️ {item['Gerät']}")
            c2.write(f"📍 {item['Standort']}")
            c3.write(f"👤 {item['Benutzer']}")
            c4.write(f"📊 {item['Status']}")

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