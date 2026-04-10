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

            if (cell) {

                let salleText;

                if (e.salle.toLowerCase().includes("amphi") || 
                    e.salle.toLowerCase().includes("labo")) {
                    salleText = e.salle;
                } else {
                    salleText = "Salle " + e.salle;
                }

              
                let bgColor = "#f8f9fa"; 

                if (e.cours.toLowerCase().includes("td") || 
                    e.cours.toLowerCase().includes("tp")) {
                    bgColor = "#fff3cd"; 
                }

                
                cell.innerHTML = `
    <div style="
        display:inline-block;
        border:1px solid #ccc;
        border-radius:6px;
        font-size:16px;
        width:140px;
        min-height:55px;
        overflow:hidden;
        background:${bgColor};
    ">

        ${
            (e.cours.toLowerCase().includes("td") || e.cours.toLowerCase().includes("tp"))
            ?
            `
            <div style="display:flex; text-align:center;">

                <!-- TD / TP -->
                <div style="
                    width:20%;
                    background:#ffeeba;
                    font-weight:bold;
                    border-right:1px solid #ccc;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">
                    ${e.cours.toLowerCase().includes("td") ? "TD" : "TP"}
                </div>

                <!-- Salle -->
                <div style="
                    width:30%;
                    font-weight:bold;
                    color:#0d6efd;
                    border-right:1px solid #ccc;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">
                    ${salleText}
                </div>

                <!-- Module -->
                <div style="
                    width:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:500;
                ">
                    ${e.cours}
                </div>

            </div>
            `
            :
            `
            <!-- Cours normal -->
            <div style="text-align:center; padding:5px;">
                <div style="
                    font-weight:bold;
                    border-bottom:1px solid #ccc;
                    margin-bottom:3px;
                    color:#0d6efd;
                ">
                    ${salleText}
                </div>
                <div>
                    ${e.cours}
                </div>
            </div>
            `
        }

    </div>
`;


            }
        });
    })
    .catch(err => console.error(err));
}







