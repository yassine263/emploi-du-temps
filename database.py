import sqlite3

DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    c = conn.cursor()

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS filiere (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS prof (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        specialite TEXT
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS salle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        capacite INTEGER,
        labo INTEGER
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS groupe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        filiere_id INTEGER
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS creneau (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temps TEXT
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS cours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prof_id INTEGER,
        groupe_id INTEGER,
        nb_etudiants INTEGER,
        besoin_labo INTEGER
    )
    """)

    conn.commit()
    conn.close() 

