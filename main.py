##
##  ChickIn! Backend
##
##  Author: Samuel Luggeri
##

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from queue import Queue
from threading import Thread

import time

app = Flask(__name__)
DB_PATH = "database.db"

barcode_queue = Queue()

# ==========================
# DATABASE
# ==========================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
# ==========================
# ROUTES
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_visit", methods=["POST"])
def add_visit():
    data = request.form
    visit_type = data.get('type')
    multiplier = int(data.get('multiplier', 1))
    timestamp = data.get('timestamp')  # formato ISO

    # Campi opzionali
    name = data.get('name')
    surname = data.get('surname')
    barcode = data.get('barcode')
    event_name = data.get('eventName')
    participants = data.get('participants')
    country = data.get('country')
    school_name = data.get('school_name')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visits (type, timestamp, multiplier, name, surname, barcode, event_name, participants, country, school_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (visit_type, timestamp, multiplier, name, surname, barcode, event_name, participants, country, school_name))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route("/visits")
def show_visits():
    conn = get_db()
    cur = conn.cursor()
    # Query sulla tabella corretta
    cur.execute("SELECT * FROM visits ORDER BY timestamp DESC")
    visits = cur.fetchall()
    conn.close()

    return render_template("visits.html", visits=visits)

# ==========================
# ENTRY POINT
# ==========================

if __name__ == "__main__":

    app.run(debug=True)