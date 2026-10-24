import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "smartlead.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def lead_ekle(isim: str, telefon: str, mesaj: str = ""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    conn.commit()
    yeni_id = cursor.lastrowid
    conn.close()
    return yeni_id

def tum_leadler():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY tarih DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
