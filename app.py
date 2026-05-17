from flask import Flask, jsonify, render_template, request
from database import connect, init_db
from backtracking import backtracking, generate_cours_list

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate")
def generate():
    filiere_id = request.args.get("filiere_id")

    conn = connect()
    c = conn.cursor()

    salles = [
        dict(zip([col[0] for col in c.description], row))
        for row in c.execute("SELECT * FROM salle")
    ]

    creneaux = [
        dict(zip([col[0] for col in c.description], row))
        for row in c.execute("SELECT * FROM creneau")
    ]

    c.execute("SELECT * FROM prof")
    cols = [col[0] for col in c.description]
    profs_list = [dict(zip(cols, row)) for row in c.fetchall()]

    profs = {p["id"]: p["prenom"] + " " + p["nom"] for p in profs_list}

    conn.close()

    cours_list = generate_cours_list(filiere_id)
    solution = backtracking(cours_list, salles, creneaux)

    result = []
    if solution:
        for s in solution:
            nom_cours = s["cours"]["nom"]
            type_cours = None

            if nom_cours.endswith("CM"):
                nom_cours = nom_cours[:-2].strip()
                type_cours = "CM"
            elif nom_cours.endswith("TD"):
                nom_cours = nom_cours[:-2].strip()
                type_cours = "TD"
            elif nom_cours.endswith("TP"):
                nom_cours = nom_cours[:-2].strip()
                type_cours = "TP"

            result.append({
                "cours": nom_cours,
                "type": type_cours,
                "salle": s["salle"]["nom"],
                "creneau": s["creneau"]["temps"],
                "prof": profs.get(s["cours"]["prof_id"], "")
            })

    return jsonify(result)




@app.route("/api/profs", methods=["GET"])
def get_profs():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM prof")
    rows = c.fetchall()
    cols = [col[0] for col in c.description]
    data = [dict(zip(cols, row)) for row in rows]
    conn.close()
    return jsonify(data)


@app.route("/api/profs", methods=["POST"])
def add_prof():
    data = request.json
    conn = connect()
    c = conn.cursor()
    c.execute("""
        INSERT INTO prof (nom, prenom, email, specialite)
        VALUES (?, ?, ?, ?)
    """, (data["nom"], data["prenom"], data["email"], data["specialite"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/profs/<int:id>", methods=["PUT"])
def update_prof(id):
    data = request.json
    conn = connect()
    c = conn.cursor()
    c.execute("""
        UPDATE prof SET nom=?, prenom=?, email=?, specialite=? WHERE id=?
    """, (data["nom"], data["prenom"], data["email"], data["specialite"], id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/profs/<int:id>", methods=["DELETE"])
def delete_prof(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM prof WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})




@app.route("/api/salles", methods=["GET"])
def get_salles():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM salle")
    cols = [col[0] for col in c.description]
    data = [dict(zip(cols, row)) for row in c.fetchall()]
    conn.close()
    return jsonify(data)


@app.route("/api/salles", methods=["POST"])
def add_salle():
    data = request.json
    conn = connect()
    c = conn.cursor()
    c.execute("""
        INSERT INTO salle (nom, capacite, labo)
        VALUES (?, ?, ?)
    """, (data["nom"], data["capacite"], data.get("labo", 0)))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/salles/<int:id>", methods=["PUT"])
def update_salle(id):
    data = request.json
    conn = connect()
    c = conn.cursor()
    c.execute("""
        UPDATE salle SET nom=?, capacite=?, labo=? WHERE id=?
    """, (data["nom"], data["capacite"], data.get("labo", 0), id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/salles/<int:id>", methods=["DELETE"])
def delete_salle(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM salle WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})


@app.route("/api/filieres", methods=["GET"])
def get_filieres():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM filiere")
    cols = [col[0] for col in c.description]
    filieres = [dict(zip(cols, row)) for row in c.fetchall()]

    result = []
    for f in filieres:
        c.execute("SELECT * FROM groupe WHERE filiere_id = ?", (f["id"],))
        gcols = [col[0] for col in c.description]
        groupes = [dict(zip(gcols, row)) for row in c.fetchall()]

        nb_td = len([g for g in groupes if "TD" in g["nom"]])
        nb_tp = len([g for g in groupes if "TP" in g["nom"]])

        c.execute("""
            SELECT COALESCE(MAX(nb_etudiants), 0)
            FROM cours
            JOIN groupe ON cours.groupe_id = groupe.id
            WHERE groupe.filiere_id = ? AND cours.nom LIKE '%CM%'
        """, (f["id"],))
        row = c.fetchone()
        nb_etudiants = row[0] if row else 0

        result.append({
            "id": f["id"],
            "nom": f["nom"],
            "nb_etudiants": nb_etudiants,
            "nb_td": nb_td,
            "nb_tp": nb_tp,
            "groupes": groupes
        })

    conn.close()
    return jsonify(result)


@app.route("/api/filieres", methods=["POST"])
def add_filiere():
    data = request.json
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO filiere (nom) VALUES (?)", (data["nom"],))
    filiere_id = c.lastrowid

    nb_td = int(data.get("nb_td", 1))
    nb_tp = int(data.get("nb_tp", 1))

    for i in range(1, nb_td + 1):
        c.execute("INSERT INTO groupe (nom, filiere_id) VALUES (?, ?)",
                  (f"TD{i}_F{filiere_id}", filiere_id))

    for i in range(1, nb_tp + 1):
        c.execute("INSERT INTO groupe (nom, filiere_id) VALUES (?, ?)",
                  (f"TP{i}_F{filiere_id}", filiere_id))

    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "id": filiere_id})


@app.route("/api/filieres/<int:id>", methods=["PUT"])
def update_filiere(id):
    data = request.json
    conn = connect()
    c = conn.cursor()

    c.execute("UPDATE filiere SET nom=? WHERE id=?", (data["nom"], id))

   
    c.execute("DELETE FROM groupe WHERE filiere_id=?", (id,))

    nb_td = int(data.get("nb_td", 1))
    nb_tp = int(data.get("nb_tp", 1))

    for i in range(1, nb_td + 1):
        c.execute("INSERT INTO groupe (nom, filiere_id) VALUES (?, ?)",
                  (f"TD{i}_F{id}", id))

    for i in range(1, nb_tp + 1):
        c.execute("INSERT INTO groupe (nom, filiere_id) VALUES (?, ?)",
                  (f"TP{i}_F{id}", id))

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/api/filieres/<int:id>", methods=["DELETE"])
def delete_filiere(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM groupe WHERE filiere_id=?", (id,))
    c.execute("DELETE FROM filiere WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

@app.route("/api/filieres/list", methods=["GET"])
def list_filieres():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM filiere")
    cols = [col[0] for col in c.description]
    data = [dict(zip(cols, row)) for row in c.fetchall()]
    conn.close()
    return jsonify(data)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
