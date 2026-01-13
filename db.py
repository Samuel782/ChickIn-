import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Tipo di visita: Biblioteca, Servizi, Turista, Evento, Cittadino, Scuole
    type TEXT NOT NULL,
    
    -- Informazioni generali
    timestamp DATETIME NOT NULL,
    multiplier INTEGER DEFAULT 1,
    
    -- Campi opzionali generali
    name TEXT,
    surname TEXT,
    barcode TEXT,
    
    -- Campi specifici per Evento
    event_name TEXT,
    participants INTEGER,
    
    -- Campi specifici per Turista
    country TEXT,
    
    -- Campi specifici per Scuole
    school_name TEXT
);
""")

conn.commit()
conn.close()