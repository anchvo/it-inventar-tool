import sqlite3


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