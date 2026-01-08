##
##  
##
##  Autor: Samuel Luggeri
##

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"


def get_db():
    return sqlite3.connect(DATABASE)

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



if __name__ == "__main__":
    app.run(debug=True)