// Se agrega un evento para que cuando se haga clic en el botón se invoque la función fetchSongs
document.getElementById("search").addEventListener("click", fetchSongs);

function fetchSongs() {
    // Se obtiene el nombre del artista ingresado en el campo de texto
    let artist = document.getElementById("artist").value.trim();

    // Si no se ingresó ningún nombre, se muestra una alerta y se detiene la función
    if (!artist) {
        alert("Por favor, ingresa el nombre de un artista.");
        return;
    }

    // Actualizar el caption de la tabla para incluir el nombre del artista
    document.getElementById("tableCaption").textContent = `Top 10 Canciones de ${artist}`;
    
    // Actualizar el caption del header para incluir el nombre del artista
    document.getElementById("headerCaption").textContent = `Encontradas top 10 canciones de ${artist}`;

    // Construir la URL de la API Lambda. Reemplaza la URL base por la de tu endpoint.
    let apiUrl = ``;

    // Se realiza la petición GET utilizando la Fetch API
    fetch(apiUrl)
        .then(response => {
            // Se verifica que la respuesta sea exitosa
            if (!response.ok) {
                throw new Error("Error en la respuesta de la API");
            }
            return response.json(); // Convertir la respuesta a JSON
            })
        .then(data => {
        // Referencia al cuerpo de la tabla donde se insertarán las filas
        let tableBody = document.getElementById("tablaDeTop10").querySelector("tbody");
        // Se limpia el contenido anterior en la tabla
        tableBody.innerHTML = "";

        // Se recorre el arreglo de canciones para crear una fila por cada canción
        data.forEach(song => {
            // Se crea una nueva fila (<tr>)
            let row = document.createElement("tr");
            // Se crea la celda para la posición y se asigna el valor correspondiente
            let cellRank = document.createElement("td");
            cellRank.textContent = song.rank;
            row.appendChild(cellRank);
            // Se crea la celda para el nombre de la canción y se asigna el valor correspondiente
            let cellName = document.createElement("td");
            cellName.textContent = song.name;
            row.appendChild(cellName);
            // Se agrega la fila completa al cuerpo de la tabla
            tableBody.appendChild(row);
        });
    })

        .catch(error => {
            // Se captura y muestra cualquier error que ocurra durante la petición
            console.error("Error al obtener los datos:", error);
            alert("Ocurrió un error al obtener los datos. Verifica la consola para más detalles.");
        });
}