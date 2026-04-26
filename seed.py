from database import connect

def seed():
    conn = connect()
    c = conn.cursor()

    
    tables = ["filiere", "prof", "salle", "cours", "creneau", "groupe"]
    for t in tables:
        c.execute(f"DELETE FROM {t}")

    
    filieres = [(i, f"Filiere {i}") for i in range(1, 11)]
    c.executemany("INSERT INTO filiere VALUES (?,?)", filieres)

    
    profs = [
        (1, "Dr Yassine"),
        (2, "Dr Ahmed"),
        (3, "Dr Ali"),
        (4, "Dr Sara"),
        (5, "Dr Fatima"),
        (6, "Dr Hassan"),
        (7, "Dr Salma"),
        (8, "Dr Karim"),
        (9, "Dr Noura"),
        (10, "Dr Imane")
    ]
    c.executemany("INSERT INTO prof VALUES (?,?)", profs)

    
    groupes = []
    gid = 1
    for f in range(1, 11):
        groupes.append((gid, f"TD1_F{f}", f))
        gid += 1
        groupes.append((gid, f"TD2_F{f}", f))
        gid += 1

    c.executemany("INSERT INTO groupe VALUES (?,?,?)", groupes)

    
    salles = []

    
    for i in range(1, 9):
        salles.append((i, f"Amphi {i}", 200, 0))

    
    sid = 9
    for i in range(1, 41):
        labo = 1 if i % 3 == 0 else 0
        salles.append((sid, str(i), 30 + (i % 10), labo))
        sid += 1

    c.executemany("INSERT INTO salle VALUES (?,?,?,?)", salles)

    
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    heures = ["08:30", "10:15", "12:00", "14:30", "16:15"]

    creneaux = []
    creneau_id = 1

    for j in jours:
        for h in heures:
            if j == "Samedi" and h in ["14:30", "16:15"]:
                continue
            creneaux.append((creneau_id, f"{j} {h}"))
            creneau_id += 1

    c.executemany("INSERT INTO creneau VALUES (?,?)", creneaux)

    
    modules = ["Algo", "BD", "Reseaux", "Python", "IA", "Systeme", "Web"]

    
    module_prof = {
        "Algo": 1,
        "BD": 2,
        "Reseaux": 3,
        "Python": 4,
        "IA": 5,
        "Systeme": 6,
        "Web": 7
    }

    cours_id = 1

    for f_id in range(1, 11):
        for g in groupes:
            if g[2] != f_id:
                continue

            groupe_id = g[0]

            
            for m in modules:
                prof_id = module_prof[m]
                cours = (
                    cours_id,
                    f"{m} CM",
                    prof_id,
                    groupe_id,
                    150,
                    0
                )
                c.execute("INSERT INTO cours VALUES (?,?,?,?,?,?)", cours)
                cours_id += 1

            
            for m in modules[:5]:
                cours = (
                    cours_id,
                    f"{m} TD",
                    None,
                    groupe_id,
                    35,
                    0
                )
                c.execute("INSERT INTO cours VALUES (?,?,?,?,?,?)", cours)
                cours_id += 1

            
            for m in modules[:2]:
                cours = (
                    cours_id,
                    f"{m} TP",
                    None,
                    groupe_id,
                    25,
                    1
                )
                c.execute("INSERT INTO cours VALUES (?,?,?,?,?,?)", cours)
                cours_id += 1

    
    conn.commit()
    conn.close()

    print("DATABASE READY - PROFS ONLY FOR CM")

if __name__ == "__main__":
    seed()

