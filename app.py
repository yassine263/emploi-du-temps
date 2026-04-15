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
                "prof": s["cours"]["prof_id"]
            })

    return jsonify(result)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

