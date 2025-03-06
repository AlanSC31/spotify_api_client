from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#credenciales para conexion con la api
app_id = '0b8cd645c7284c1aa9519857fbccd9ca'
secret_id = 'a8c395d102c74bf9b7915f18ed2dfc8d'

#inicializar api con spotipy con autenticacion
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
sp = spotipy.Spotify(auth_manager=auth_manager)

#home route
@app.route("/")
def home():
    return 'Spotify api client'

#search route
@app.route('/search', methods=['GET'])
def artist_top_ten():
    #se obtiene el artista de los parametros de la consulta, se coloca valor por defecto
    artist_name = request.args.get('artist', 'Bad Bunny')
    #busca en el api el artista que se paso en parametros y retorna la respuesta en json
    result = sp.search(q=artist_name, type='artist')

    # Obtener el ID del primer artista que aparece en los resultados
    artist_id = result['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)
    
    #extrae los nombres de las canciones y enumerar
    top_10_tracks = []
    for idx, track in enumerate(top_tracks['tracks'][:10], start=1):  
        track_info = {
            'rank': idx,  
            'name': track['name'],
        }
        # agrega a la lista los resultados
        top_10_tracks.append(track_info)
    
    # Devolver la lista del top 10
    return jsonify(top_10_tracks)


if __name__ == "__main__":
    app.run(debug=True)