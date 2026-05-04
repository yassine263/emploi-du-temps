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

    profs = {p["id"]: p["nom"] for p in profs_list}

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


@app.route('/gestion')
def gestion():
    return render_template('gestion.html')




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

    c.execute("INSERT INTO prof (nom) VALUES (?)", (data["nom"],))

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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
