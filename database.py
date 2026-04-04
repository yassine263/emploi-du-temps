import sqlite3

def connect():
    return sqlite3.connect("database.db")


def init_db():
    conn = connect()
    c = conn.cursor()

    # Filiere
    c.execute("""
    CREATE TABLE IF NOT EXISTS filiere (
        id INTEGER PRIMARY KEY,
        nom TEXT
    )
    """)

    # Prof
    c.execute("""
    CREATE TABLE IF NOT EXISTS prof (
        id INTEGER PRIMARY KEY,
        nom TEXT
    )
    """)

    # Groupe (TD/TP)
    c.execute("""
    CREATE TABLE IF NOT EXISTS groupe (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        filiere_id INTEGER
    )
    """)

    # Salle
    c.execute("""
    CREATE TABLE IF NOT EXISTS salle (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        capacite INTEGER,
        labo INTEGER
    )
    """)

    # Cours
    c.execute("""
    CREATE TABLE IF NOT EXISTS cours (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prof_id INTEGER,
        groupe_id INTEGER,
        nb_etudiants INTEGER,
        besoin_labo INTEGER
    )
    """)

    # Créneaux
    c.execute("""
    CREATE TABLE IF NOT EXISTS creneau (
        id INTEGER PRIMARY KEY,
        temps TEXT
    )
    """)

    conn.commit()
    conn.close()
