from database import connect
import random

def generate_cours_list(filiere_id):
    conn = connect()
    c = conn.cursor()

    c.execute("""
        SELECT cours.* 
        FROM cours
        JOIN groupe ON cours.groupe_id = groupe.id
        WHERE groupe.filiere_id = ?
    """, (filiere_id,))
    
    rows = c.fetchall()
    columns = [col[0] for col in c.description]
    all_cours = [dict(zip(columns, row)) for row in rows]

    conn.close()
    groupes = list(set([c["groupe_id"] for c in all_cours]))

    if not groupes:
        return []

    gid = groupes[0]   

    cm = [c for c in all_cours if c["groupe_id"] == gid and "CM" in c["nom"]][:7]
    td = [c for c in all_cours if c["groupe_id"] == gid and "TD" in c["nom"]][:5]
    tp = [c for c in all_cours if c["groupe_id"] == gid and "TP" in c["nom"]][:2]

    cours_list = cm + td + tp

    return cours_list


def is_valid(solution, cours, salle, creneau):
    for s in solution:
        
        if s["salle"]["id"] == salle["id"] and s["creneau"]["id"] == creneau["id"]:
            return False
    
        if s["cours"]["prof_id"] == cours["prof_id"] and s["creneau"]["id"] == creneau["id"]:
            return False
        if cours["groupe_id"] != 0:
            if s["cours"]["groupe_id"] == cours["groupe_id"] and s["creneau"]["id"] == creneau["id"]:
                return False
    if cours["nb_etudiants"] > salle["capacite"]:
        return False
    if cours["besoin_labo"] == 1 and salle["labo"] == 0:
        return False
    return True

def backtracking(cours_list, salles, creneaux, solution=None, index=0):
    if solution is None:
        solution = []

    if index >= len(cours_list):
        return solution  

    cours = cours_list[index]

    if "CM" in cours["nom"]:
        salles_possibles = [s for s in salles if s["capacite"] >= 150]
    else:
        salles_possibles = [s for s in salles if s["capacite"] < 150]

    random.shuffle(salles_possibles)
    random.shuffle(creneaux)

    for creneau in creneaux:
        for salle in salles_possibles:
            if is_valid(solution, cours, salle, creneau):
                solution.append({"cours": cours, "salle": salle, "creneau": creneau})
                result = backtracking(cours_list, salles, creneaux, solution, index + 1)
                if result:
                    return result
                solution.pop()

    return None




