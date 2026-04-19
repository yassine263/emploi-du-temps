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

                if (e.type === "TD" || e.type === "TP") {
                    bgColor = "#fff3cd"; 
                }

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
                ">

                    ${
                        (e.type === "TD" || e.type === "TP")
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
                                ${e.type}
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
                                font-size:12px;
                            ">
                                ${salleText}
                            </div>

                            <!-- Module + Prof -->
                            <div style="
                                width:50%;
                                display:flex;
                                flex-direction:column;
                                align-items:center;
                                justify-content:center;
                                font-size:12px;
                            ">
                                <div>${e.cours}</div>
                                <div style="font-size:10px; color:#555;">
                                    ${e.prof}
                                </div>
                            </div>

                        </div>
                        `
                        :
                        `
                        <!-- CM -->
                        <div style="text-align:center; padding:5px;">
                            <div style="
                                font-weight:bold;
                                border-bottom:1px solid #ccc;
                                margin-bottom:3px;
                                color:#0d6efd;
                            ">
                                ${salleText}
                            </div>

                            <div>${e.cours}</div>

                            <div style="font-size:11px; color:#555;">
                                ${e.prof}
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

