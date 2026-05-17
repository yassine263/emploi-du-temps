from database import connect
import random


def get_random_prof(conn):
    c = conn.cursor()
    c.execute("SELECT id FROM prof")
    profs = [row[0] for row in c.fetchall()]
    return random.choice(profs) if profs else None


FILIERES = {
    "S1": {
        "S1 Tronc Commun MI": ["Analyse 1", "Algebre 1", "Info 1", "Physique 1", "Anglais"],
        "S1 Tronc Commun PC": ["Analyse 1", "Algebre 1", "Chimie 1", "Physique 1", "Anglais"],
    },
    "S2": {
        "S2 Tronc Commun MI": ["Analyse 2", "Algebre 2", "Info 2", "Physique 2", "Francais"],
        "S2 Tronc Commun PC": ["Analyse 2", "Algebre 2", "Chimie 2", "Physique 2", "Francais"],
    },
    "S3": {
        "S3 MI": ["Analyse 3", "Algebre 3", "Programmation", "Electronique", "Proba"],
        "S3 PC": ["Thermodynamique", "Optique", "Chimie Organique", "Algebre 3", "Proba"],
    },
    "S4": {
        "S4 MI": ["Analyse 4", "Systemes", "Reseaux", "POO", "Statistiques"],
        "S4 PC": ["Mecanique", "Electromagnetisme", "Chimie Analytique", "Statistiques", "POO"],
    },
    "S5": {
        "S5 MI": ["IA", "BD", "Compilation", "Systemes Distribues", "Securite"],
        "S5 Math": ["Topologie", "Analyse Fonctionnelle", "Algebre 5", "Probabilites", "Geometrie"],
    },
    "S6": {
        "S6 2IDL": ["Genie Logiciel", "Architecture", "DevOps", "Machine Learning", "PFE"],
        "S6 P_IME": ["Mathematiques Appliquees", "Modelisation", "Simulation", "Optimisation", "PFE"],
    },
}


def seed():
    conn = connect()
    c = conn.cursor()

   
    tables = ["filiere", "prof", "salle", "cours", "creneau", "groupe"]
    for t in tables:
        c.execute(f"DELETE FROM {t}")

   
    profs = [
        ("Yassine", "Dr", "yassine@univ.ma", "Algo"),
        ("Ahmed",   "Dr", "ahmed@univ.ma",   "BD"),
        ("Ali",     "Dr", "ali@univ.ma",     "Reseaux"),
        ("Sara",    "Dr", "sara@univ.ma",    "Python"),
        ("Fatima",  "Dr", "fatima@univ.ma",  "IA"),
        ("Hassan",  "Dr", "hassan@univ.ma",  "Systeme"),
        ("Salma",   "Dr", "salma@univ.ma",   "Web"),
        ("Karim",   "Dr", "karim@univ.ma",   "Algo"),
        ("Noura",   "Dr", "noura@univ.ma",   "BD"),
        ("Imane",   "Dr", "imane@univ.ma",   "IA"),
        ("Rachid",  "Dr", "rachid@univ.ma",  "Maths"),
        ("Zineb",   "Dr", "zineb@univ.ma",   "Physique"),
        ("Omar",    "Dr", "omar@univ.ma",    "Chimie"),
        ("Laila",   "Dr", "laila@univ.ma",   "Analyse"),
        ("Younes",  "Dr", "younes@univ.ma",  "Algebre"),
    ]
    c.executemany("""
        INSERT INTO prof (nom, prenom, email, specialite)
        VALUES (?, ?, ?, ?)
    """, profs)

    
    salles = []
    for i in range(1, 9):
        salles.append((i, f"Amphi {i}", 200, 0))
    sid = 9
    for i in range(1, 41):
        labo = 1 if i % 3 == 0 else 0
        salles.append((sid, str(i), 30 + (i % 10), labo))
        sid += 1
    c.executemany("INSERT INTO salle VALUES (?,?,?,?)", salles)

    
    jours  = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    heures = ["08:30", "10:15", "12:00", "14:30", "16:15"]
    creneaux = []
    cid = 1
    for j in jours:
        for h in heures:
            if j == "Samedi" and h in ["14:30", "16:15"]:
                continue
            creneaux.append((cid, f"{j} {h}"))
            cid += 1
    c.executemany("INSERT INTO creneau VALUES (?, ?)", creneaux)

    
    filiere_id = 1
    groupe_id  = 1
    cours_id   = 1

    for semestre, filieres in FILIERES.items():
        for filiere_nom, modules in filieres.items():

            
            c.execute("INSERT INTO filiere (id, nom) VALUES (?, ?)",
                      (filiere_id, filiere_nom))

            
            groupes_ids = []
            for gi in range(1, 3):
                c.execute("INSERT INTO groupe (id, nom, filiere_id) VALUES (?, ?, ?)",
                          (groupe_id, f"TD{gi}_{filiere_nom}", filiere_id))
                groupes_ids.append(groupe_id)
                groupe_id += 1

            
            tp_groupes_ids = []
            for gi in range(1, 3):
                c.execute("INSERT INTO groupe (id, nom, filiere_id) VALUES (?, ?, ?)",
                          (groupe_id, f"TP{gi}_{filiere_nom}", filiere_id))
                tp_groupes_ids.append(groupe_id)
                groupe_id += 1

            
            for module in modules:
                prof_id = get_random_prof(conn)

                
                c.execute("""
                    INSERT INTO cours (id, nom, prof_id, groupe_id, nb_etudiants, besoin_labo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (cours_id, f"{module} CM", prof_id, groupes_ids[0], 150, 0))
                cours_id += 1

                
                for gid in groupes_ids:
                    c.execute("""
                        INSERT INTO cours (id, nom, prof_id, groupe_id, nb_etudiants, besoin_labo)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (cours_id, f"{module} TD", prof_id, gid, 35, 0))
                    cours_id += 1

                
                for gid in tp_groupes_ids:
                    c.execute("""
                        INSERT INTO cours (id, nom, prof_id, groupe_id, nb_etudiants, besoin_labo)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (cours_id, f"{module} TP", prof_id, gid, 25, 1))
                    cours_id += 1

            filiere_id += 1

    conn.commit()
    conn.close()

    print("DATABASE READY ")
    print("\nFilières créées:")
    for sem, filieres in FILIERES.items():
        for nom in filieres:
            print(f"  {nom}")


if __name__ == "__main__":
    seed()
