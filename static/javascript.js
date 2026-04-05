function generate(){
    const filiere_id = document.getElementById("filiere").value;

    fetch(`/generate?filiere_id=${filiere_id}`)
    .then(res => res.json())
    .then(data => {

        
        document.querySelectorAll("td:not(.time)").forEach(td => {
            td.innerHTML = ""
        })

        
        data.forEach(e => {
            let cell = document.getElementById(e.creneau)

            if(cell){
                let salleText;


if (e.salle.toLowerCase().includes("amphi") || e.salle.toLowerCase().includes("labo")) {
    salleText = e.salle;
} else {
    salleText = "Salle " + e.salle;
}

cell.innerHTML = `
    <div class="course">
        <strong>${e.cours}</strong><br>
        ${salleText}
    </div>
`;

            }
        })
    })
}








