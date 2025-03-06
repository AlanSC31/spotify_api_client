import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Credenciales de la API de Spotify
app_id = '0b8cd645c7284c1aa9519857fbccd9ca'
secret_id = 'a8c395d102c74bf9b7915f18ed2dfc8d'

# Inicializar la API con Spotify y autenticación
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
sp = spotipy.Spotify(auth_manager=auth_manager)

def lambda_handler(event, context):
    # Obtiene el nombre del artista de los parámetros de la consulta 
    artist_name = event['queryStringParameters'].get('artist', 'Bad Bunny') #valor por defecto
    
    try:
        # Busca el artista usando la API de Spotify
        result = sp.search(q=artist_name, type='artist')

        # Obtener el ID del primer artista en los resultados
        artist_id = result['artists']['items'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id)

        # Extraer los nombres de las canciones y enumerarlas
        top_10_tracks = []
        for idx, track in enumerate(top_tracks['tracks'][:10], start=1):
            track_info = {
                'rank': idx,
                'name': track['name'],
            }
            top_10_tracks.append(track_info)

        # Responder con el top 10 de canciones en formato JSON
        response = {
            'statusCode': 200,
            'body': json.dumps(top_10_tracks),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        return response

    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        return response
