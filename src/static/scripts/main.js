/* LISTENERS */
// Documento
document.addEventListener('DOMContentLoaded', cargarTopologia);

/* FUNCIONES */
async function cargarTopologia() { // Consultamos la API para obtener la topologia
    const response = await fetch('/topologia',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'ip': '192.168.0.1',
                'name': 'enrutador1',
                'user': 'root',
                'password': 'root'
            })
        }
    );
    // Obtenemos la imagen y la asignamos
    const blob = await response.blob();
    document.querySelector("#imagen-topologia").src = window.URL.createObjectURL(blob);
};
