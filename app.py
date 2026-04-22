import streamlit as st
import sqlite3
import uuid


# Initialisierung der Datenbank
def init_db():
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS inventar (
            id TEXT PRIMARY KEY,
            geraet TEXT,
            standort TEXT,
            benutzer TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# CREATE Funktion
def add_item(item):
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO inventar (id, geraet, standort, benutzer, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        item["id"],
        item["Gerät"],
        item["Standort"],
        item["Benutzer"],
        item["Status"]
    ))

    conn.commit()
    conn.close()


# READ Funktionen
def get_items():
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("SELECT * FROM inventar")
    rows = c.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "Gerät": r[1],
            "Standort": r[2],
            "Benutzer": r[3],
            "Status": r[4]
        }
        for r in rows
    ]


def get_item_by_id(item_id):
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("SELECT * FROM inventar WHERE id = ?", (item_id,))
    row = c.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "Gerät": row[1],
            "Standort": row[2],
            "Benutzer": row[3],
            "Status": row[4]
        }
    return None


# UPDATE Funktion
def update_item(item):
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("""
        UPDATE inventar
        SET geraet=?, standort=?, benutzer=?, status=?
        WHERE id=?
    """, (
        item["Gerät"],
        item["Standort"],
        item["Benutzer"],
        item["Status"],
        item["id"]
    ))

    conn.commit()
    conn.close()


#DELETE Funktion
def delete_item(item_id):
    conn = sqlite3.connect("inventar.db")
    c = conn.cursor()

    c.execute("DELETE FROM inventar WHERE id=?", (item_id,))

    conn.commit()
    conn.close()


# UI Setup
st.set_page_config(
    page_title="IT Inventar Tool",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Inventar Tool")

# Initialisierung der Nachrichten
if "message" not in st.session_state:
    st.session_state.message = None

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
    edit_item = get_item_by_id(st.session_state.edit_id)

# Default-Werte für Create-Modus
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

    status_list = ["Aktiv", "Defekt", "Reserve"]

    status = st.selectbox(
        "Status",
        status_list,
        index=status_list.index(default_status) if default_status in status_list else 0
    )

    submitted = st.form_submit_button("Speichern")

    if submitted:
        if geraet:

            if st.session_state.edit_mode:
                # UPDATE
                update_item({
                    "id": st.session_state.edit_id,
                    "Gerät": geraet,
                    "Standort": standort,
                    "Benutzer": benutzer,
                    "Status": status
                })

                st.session_state.message = "✏️ Gerät aktualisiert!"

                st.session_state.edit_mode = False
                st.session_state.edit_id = None

                st.session_state.form_counter += 1
                st.rerun()

            else:
                # CREATE
                add_item({
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
inventar = get_items()
if inventar:

    # Suchfilter anwenden
    filtered = inventar

    if search:
        filtered = [
            item for item in filtered
            if search.lower() in item["Gerät"].lower()
            or search.lower() in item["Standort"].lower()
            or search.lower() in item["Benutzer"].lower()
            or search.lower() in item["Status"].lower()
        ]

    # Anzeige der Inventareinträge
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
                delete_item(item["id"])
                st.rerun()

else:
    st.info("Noch keine Geräte vorhanden")