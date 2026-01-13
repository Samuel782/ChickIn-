##
##  ChickIn! Backend
##
##  Author: Samuel Luggeri
##

from flask import Flask, render_template, request, redirect, url_for, send_file
import datetime
import sqlite3
from queue import Queue
from threading import Thread
from generatePdf import genera_report_pdf
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
    country = data.get('country')
    school_name = data.get('school_name')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visits (type, timestamp, multiplier, name, surname, barcode, event_name, country, school_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (visit_type, timestamp, multiplier, name, surname, barcode, event_name, country, school_name))

    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route("/visits")
def show_visits():
    conn = get_db()
    cur = conn.cursor()
    # Query sulla tabella corretta
    cur.execute("SELECT * FROM visits ORDER BY timestamp DESC")
    visits = cur.fetchall()
    conn.close()

    return render_template("visits.html", visits=visits)

@app.route("/generate_report")
def generate_report():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return "Errore: date mancanti", 400

    start = f"{start_date}T00:00"
    end = f"{end_date}T23:59"

    conn = get_db()
    cur = conn.cursor()

    # Totale visite
    cur.execute("""
        SELECT SUM(multiplier) AS totale_visite
        FROM visits
        WHERE timestamp BETWEEN ? AND ?
    """, (start, end))
    totale = cur.fetchone()['totale_visite'] or 0

    # Visite per categoria
    cur.execute("""
        SELECT
            SUM(CASE WHEN type='Biblioteca' THEN multiplier ELSE 0 END) AS biblioteca,
            SUM(CASE WHEN type='Evento' THEN multiplier ELSE 0 END) AS evento,
            SUM(CASE WHEN type='Turista' THEN multiplier ELSE 0 END) AS turisti,
            SUM(CASE WHEN type='Cittadino' THEN multiplier ELSE 0 END) AS cittadini,
            SUM(CASE WHEN type='Servizi' THEN multiplier ELSE 0 END) AS servizi,
            SUM(CASE WHEN type='Scuole' THEN multiplier ELSE 0 END) AS scuole
        FROM visits
        WHERE timestamp BETWEEN ? AND ?
    """, (start, end))
    categorie = cur.fetchone()

    conn.close()

    
    biblioteca  =    categorie[0] or 0
    evento      =    categorie[1] or 0
    turisti     =    categorie[2] or 0
    cittadini   =    categorie[3] or 0
    servizi     =    categorie[4] or 0
    scuole      =    categorie[5] or 0

    
    pdf_path = f"Santa_Bibblioteca_Report_{end}.pdf"

    genera_report_pdf(
        pdf_path,
        start_day=start_date,
        end_day=end_date,
        totale=totale,
        servizi=servizi,
        evento=evento,
        biblioteca=biblioteca,
        turisti=turisti,
        scuole=scuole,
        cittadini=cittadini
    )

    return send_file(pdf_path, as_attachment=True)

# Error handler 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ==========================
# ENTRY POINT
# ==========================

if __name__ == "__main__":

    app.run(debug=True)