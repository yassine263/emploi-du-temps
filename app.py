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
            result.append({
                "cours": s["cours"]["nom"],
                "salle": s["salle"]["nom"],
                "creneau": s["creneau"]["temps"],
                "prof": s["cours"]["prof_id"]
            })

    return jsonify(result)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
