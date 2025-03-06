# Se importan las librerías necesarias:
# Flask para crear la aplicación web, y las funciones request y jsonify para manejar las peticiones HTTP y respuestas en formato JSON.
from flask import Flask, request, jsonify
# Se importa la librería Spotipy para interactuar con la API de Spotify.
import spotipy
# Se importa el manejador de autenticación que permite usar las credenciales del cliente.
from spotipy.oauth2 import SpotifyClientCredentials

# Se crea una instancia de la aplicación Flask.
app = Flask(__name__)

# Credenciales para la conexión con la API de Spotify.
# Estas credenciales (app_id y secret_id) deben ser obtenidas desde el dashboard de Spotify Developer.
app_id = '5937743c44c34e5495711416385e15de'
secret_id = '6c592d5129ee4761a1c316cd1384af59'

# Inicialización del autenticador de Spotify con las credenciales proporcionadas.
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
# Se crea un objeto 'sp' de la clase Spotify, el cual nos permite realizar llamadas a la API de Spotify.
sp = spotipy.Spotify(auth_manager=auth_manager)

# Ruta raíz de la aplicación. Cuando se accede a la URL base, se muestra un mensaje simple.
@app.route("/")
def home():
    return 'Agrega al URL: /search?artist="artista"'

# Ruta '/search' que acepta peticiones GET para buscar un artista y obtener su top 10 de canciones.
@app.route('/search', methods=['GET'])
def artist_top_ten():
    # Se obtiene el parámetro 'artist' de la URL; si no se especifica, se utiliza 'NSQK' como valor por defecto.
    artist_name = request.args.get('artist', 'NSQK')
    
    # Se realiza una búsqueda en Spotify para encontrar al artista especificado.
    # El parámetro 'type' se establece en 'artist' para limitar la búsqueda a artistas.
    result = sp.search(q=artist_name, type='artist')
    
    # Se extrae el ID del primer artista que aparece en los resultados de la búsqueda.
    artist_id = result['artists']['items'][0]['id']
    
    # Se obtiene el listado de las canciones más populares (top tracks) del artista, utilizando su ID.
    top_tracks = sp.artist_top_tracks(artist_id)
    
    # Se prepara una lista para almacenar la información de las 10 canciones más populares.
    top_10_tracks = []
    # Se itera sobre las primeras 10 canciones del resultado, utilizando enumerate para asignar un ranking.
    for idx, track in enumerate(top_tracks['tracks'][:10], start=1):  
        # Se crea un diccionario con la información deseada: el ranking y el nombre de la canción.
        track_info = {
            'rank': idx,  
            'name': track['name'],
        }
        # Se agrega la información de la canción a la lista.
        top_10_tracks.append(track_info)
    
    # Se retorna la lista de canciones en formato JSON, lo que facilita su consumo por parte de clientes o aplicaciones.
    return jsonify(top_10_tracks)

# Se indica que la aplicación se ejecute sólo cuando se ejecuta este script directamente.
if __name__ == "__main__":
    # Se inicia la aplicación Flask en modo debug, lo que permite ver detalles en caso de errores.
    app.run(debug=True)