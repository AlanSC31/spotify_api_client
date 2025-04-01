import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# credenciales de la API
app_id = '0b8cd645c7284c1aa9519857fbccd9ca'
secret_id = 'a8c395d102c74bf9b7915f18ed2dfc8d'

# inicializar la API con autenticación
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_top_tracks(artist_name):
    """Obtiene las 10 canciones más populares de un artista en Spotify."""
    if not artist_name:
        return None, "Ingresa el nombre de un artista"

    try:
        result = sp.search(q=artist_name, type='artist')
        if not result['artists']['items']:
            return None, "Artista no encontrado"

        # selecciona el primer resultado de la búsqueda de artista
        artist = result['artists']['items'][0]
        artist_id = artist['id']
        artist_name = artist['name']  # obtener el nombre exacto del artista
        
        # obtener el top del artista
        top_tracks = sp.artist_top_tracks(artist_id)

        # lista con las 10 mejores canciones
        songs = [track['name'] for track in top_tracks['tracks'][:10]]
        return artist_name, songs

    except Exception as e:
        return None, str(e)

