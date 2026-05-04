
function generate() {
    const filiere_id = document.getElementById("filiere").value;

    fetch(`/generate?filiere_id=${filiere_id}`)
        .then(res => res.json())
        .then(data => {

            
            document.querySelectorAll("td:not(.time)").forEach(td => {
                td.innerHTML = "";
            });

            data.forEach(e => {
                let cell = document.getElementById(e.creneau);
                if (!cell) return;

                let salleText = (
                    e.salle.toLowerCase().includes("amphi") ||
                    e.salle.toLowerCase().includes("labo")
                ) ? e.salle : "Salle " + e.salle;

                let bgColor = (e.type === "TD" || e.type === "TP")
                    ? "#fff3cd"
                    : "#f8f9fa";

                cell.innerHTML = `
                    <div style="
                        display:inline-block;
                        border:1px solid #ccc;
                        border-radius:4px;
                        font-size:14px;
                        width:150px;
                        min-height:55px;
                        overflow:hidden;
                        background:${bgColor};
                        text-align:center;
                        padding:5px;
                    ">
                        <div style="font-weight:bold;color:#0d6efd;">
                            ${salleText}
                        </div>

                        <div>${e.cours}</div>

                        <div style="font-size:11px;color:#555;">
                            ${e.prof}
                        </div>
                    </div>
                `;
            });
        })
        .catch(err => console.error(err));
}



async function loadProfs() {
    const res = await fetch("/api/profs");
    const data = await res.json();

    const tbody = document.getElementById("profs-tbody");
    tbody.innerHTML = "";

    data.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.nom}</td>
                <td>${p.prenom}</td>
                <td>${p.email || ""}</td>
                <td>${p.specialite || ""}</td>
                <td>
                    <button onclick="deleteProf(${p.id})"> Supprimer</button>
                </td>
            </tr>
        `;
    });
}



async function addProf() {

    const data = {
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        email: document.getElementById("email").value,
        specialite: document.getElementById("specialite").value
    };

    await fetch("/api/profs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    
    document.getElementById("form-prof").reset();
    loadProfs();
}



async function deleteProf(id) {
    await fetch(`/api/profs/${id}`, {
        method: "DELETE"
    });

    loadProfs();
}


document.addEventListener("DOMContentLoaded", () => {
    loadProfs();
});



