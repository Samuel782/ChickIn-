##
##  ChickIn! Backend
##
##  Author: Samuel Luggeri
##

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from queue import Queue
from threading import Thread
from barcode_reader import barcode_listener
import time

app = Flask(__name__)
DATABASE = "database.db"

barcode_queue = Queue()

# ==========================
# DATABASE
# ==========================

def get_db():
    return sqlite3.connect(DATABASE, check_same_thread=False)


def save_barcode(barcode):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scans (barcode, timestamp) VALUES (?, datetime('now'))",
        (barcode,)
    )
    conn.commit()
    conn.close()


# ==========================
# BARCODE HANDLER
# ==========================

def handle_barcode(barcode: str):
    print("Received:", barcode)
    barcode_queue.put(barcode)


def barcode_worker():
    while True:
        barcode = barcode_queue.get()
        save_barcode(barcode)


# ==========================
# START BACKGROUND THREADS
# ==========================

def start_background_threads():
    Thread(
        target=barcode_listener,
        args=(handle_barcode,),
        daemon=True
    ).start()

    Thread(
        target=barcode_worker,
        daemon=True
    ).start()


# ==========================
# ROUTES
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_visit", methods=["POST"])
def add_visit():
    barcode = request.form.get("barcode")
    visit_type = request.form.get("type")
    timestamp = request.form.get("timestamp")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scans (barcode, type, timestamp) VALUES (?, ?, ?)",
        (barcode, visit_type, timestamp)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))


@app.route("/visits")
def show_visits():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM scans ORDER BY timestamp DESC")
    visits = cur.fetchall()
    conn.close()

    return render_template("visits.html", visits=visits)


# ==========================
# ENTRY POINT
# ==========================

if __name__ == "__main__":
    start_background_threads()
    app.run(debug=False)