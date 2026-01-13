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
DATABASE = "database.db"

barcode_queue = Queue()

# ==========================
# DATABASE
# ==========================

def get_db():
    return sqlite3.connect(DATABASE, check_same_thread=False)

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
    name = request.form.get("name")
    surname = request.form.get("surname")
    timestamp = request.form.get("timestamp")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scans (barcode, type, name, surname, timestamp) VALUES (?, ?, ?, ?, ?)",
        (barcode, visit_type, name, surname, timestamp)
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

    app.run(debug=True)