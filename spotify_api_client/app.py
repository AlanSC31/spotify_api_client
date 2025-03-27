# Importar el módulo tkinter para la interfaz gráfica y renombrarlo como "tk"
import tkinter as tk
# Importar el submódulo messagebox de tkinter para mostrar mensajes de alerta, advertencia o error
from tkinter import messagebox
# Importar la librería spotipy para interactuar con la API de Spotify
import spotipy
# Importar el manejador de autenticación para la API de Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# ------------------------- Configuración de la API -------------------------
# Definir la credencial "client_id" de la API de Spotify
app_id = '0b8cd645c7284c1aa9519857fbccd9ca'
# Definir la credencial "client_secret" de la API de Spotify
secret_id = 'a8c395d102c74bf9b7915f18ed2dfc8d'

# Inicializar la autenticación de la API usando las credenciales proporcionadas
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
# Crear un objeto de la API de Spotify que se usará para realizar consultas
sp = spotipy.Spotify(auth_manager=auth_manager)

# ------------------------- Función para obtener las mejores canciones -------------------------
def get_top_tracks():
    # Obtener y limpiar el nombre del artista ingresado en el campo de texto
    artist_name = entry.get().strip()
    # Verificar si el campo de entrada está vacío y mostrar una advertencia en ese caso
    if not artist_name:
        messagebox.showwarning("Advertencia", "Ingresa el nombre de un artista")
        return
    
    try:
        # Realizar una búsqueda en la API de Spotify usando el nombre del artista proporcionado
        result = sp.search(q=artist_name, type='artist')
        # Si no se encuentra ningún artista, mostrar un mensaje de error y salir de la función
        if not result['artists']['items']:
            messagebox.showerror("Error", "Artista no encontrado")
            return

        # Seleccionar el primer resultado de la búsqueda, que se asume es el artista correcto
        artist = result['artists']['items'][0]
        # Extraer el identificador único del artista
        artist_id = artist['id']
        # Obtener el nombre exacto del artista según los datos de Spotify
        artist_name = artist['name']  
        # Solicitar las canciones más populares del artista usando su ID
        top_tracks = sp.artist_top_tracks(artist_id)

        # Habilitar el widget de texto para permitir modificaciones
        text_widget.config(state=tk.NORMAL)
        # Limpiar el contenido previo del widget de texto
        text_widget.delete("1.0", tk.END)
        # Actualizar la etiqueta del artista mostrando su nombre y un estilo decorativo
        artist_label.config(text=f"🎵 {artist_name} - Top 10 🎵")  
        
        # Iterar sobre las 10 primeras canciones del top del artista, enumerándolas
        for idx, track in enumerate(top_tracks['tracks'][:10], start=1):
            # Insertar cada canción en el widget de texto con su posición y nombre
            text_widget.insert(tk.END, f"{idx}. {track['name']}\n\n")
        
        # Deshabilitar el widget de texto para evitar modificaciones posteriores
        text_widget.config(state=tk.DISABLED)
        # Limpiar el campo de entrada para permitir una nueva búsqueda
        entry.delete(0, tk.END)  
    
    # Capturar cualquier excepción que ocurra durante el proceso y mostrar un mensaje de error
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------------- Configuración de la ventana principal -------------------------
# Crear la ventana principal de la aplicación
root = tk.Tk()
# Establecer el título de la ventana
root.title("spotify web api")
# Definir las dimensiones de la ventana (ancho x alto)
root.geometry("350x600")
# Desactivar la opción de redimensionar la ventana
root.resizable(False, False)
# Configurar el color de fondo de la ventana con el color característico de Spotify
root.configure(bg="#1DB954")

# ------------------------- Creación y configuración de widgets -------------------------
# Crear un frame (marco) para centrar los elementos dentro de la ventana principal y asignar su color de fondo
frame = tk.Frame(root, bg="#1DB954")
# Ubicar el frame con un padding vertical para separar del borde superior
frame.pack(pady=20)

# Crear y configurar la etiqueta de título que muestra "Top 10 Canciones"
title_label = tk.Label(frame, text="Top 10 Canciones", font=("Arial", 16, "bold"), bg="#1DB954", fg="white")
# Ubicar la etiqueta de título dentro del frame
title_label.pack()

# Crear un campo de entrada (Entry) para que el usuario ingrese el nombre del artista
entry = tk.Entry(frame, width=20, font=("Arial", 14), justify='center')
# Ubicar el campo de entrada con un padding vertical
entry.pack(pady=10)

# Crear un botón que al hacer clic ejecuta la función get_top_tracks para buscar las canciones
search_button = tk.Button(frame, text="Buscar", font=("Arial", 12), bg="#191414", fg="white", command=get_top_tracks)
# Ubicar el botón dentro del frame con un padding vertical
search_button.pack(pady=5)

# Crear una etiqueta para mostrar el nombre del artista seleccionado, inicialmente vacía
artist_label = tk.Label(root, text="", font=("Arial", 14, "bold italic"), bg="#1DB954", fg="white")
# Ubicar la etiqueta en la ventana principal con un padding vertical
artist_label.pack(pady=5)

# Crear un widget de texto para mostrar la lista de canciones obtenida, con configuración de tamaño y estilo
text_widget = tk.Text(root, width=35, height=20, font=("Arial", 12), bg="#FFFFFF", fg="#191414", wrap=tk.WORD)
# Ubicar el widget de texto en la ventana principal con un padding vertical
text_widget.pack(pady=10)
# Inicialmente, deshabilitar el widget de texto para evitar edición directa por el usuario
text_widget.config(state=tk.DISABLED)

# ------------------------- Ejecución de la aplicación -------------------------
# Iniciar el bucle principal de la aplicación para esperar y responder a eventos del usuario
root.mainloop()
