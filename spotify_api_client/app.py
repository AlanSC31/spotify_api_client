import tkinter as tk
from tkinter import messagebox
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# credenciales de la API
app_id = '0b8cd645c7284c1aa9519857fbccd9ca'
secret_id = 'a8c395d102c74bf9b7915f18ed2dfc8d'

# inicializar la API con autenticación
auth_manager = SpotifyClientCredentials(client_id=app_id, client_secret=secret_id)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_top_tracks():
    artist_name = entry.get().strip()
    if not artist_name:
        messagebox.showwarning("Advertencia", "Ingresa el nombre de un artista")
        return
    
    try:
        result = sp.search(q=artist_name, type='artist')
        if not result['artists']['items']:
            messagebox.showerror("Error", "Artista no encontrado")
            return

        # selecciona el primer resultado de la busqueda de artista
        artist = result['artists']['items'][0]
        # guarda el id del artista
        artist_id = artist['id']
        # obtener el nombre exacto del artista
        artist_name = artist['name']  
        # guarda el top del artista
        top_tracks = sp.artist_top_tracks(artist_id)

        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        # mostrar el nombre del artista con estilo
        artist_label.config(text=f"🎵 {artist_name} - Top 10 🎵")  
        
        # enumera y limita el top a 10 resultados 
        for idx, track in enumerate(top_tracks['tracks'][:10], start=1):
            text_widget.insert(tk.END, f"{idx}. {track['name']}\n\n")
        
        text_widget.config(state=tk.DISABLED)
        # Limpiar el campo de entrada después de buscar
        entry.delete(0, tk.END)  
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ventana principal
root = tk.Tk()
root.title("spotify web api")
root.geometry("350x600")
root.resizable(False, False)
root.configure(bg="#1DB954")

# frame para centrar los elementos
frame = tk.Frame(root, bg="#1DB954")
frame.pack(pady=20)

# titulo
title_label = tk.Label(frame, text="Top 10 Canciones", font=("Arial", 16, "bold"), bg="#1DB954", fg="white")
title_label.pack()

# barra busqueda
entry = tk.Entry(frame, width=20, font=("Arial", 14), justify='center')
entry.pack(pady=10)

# button buscar
search_button = tk.Button(frame, text="Buscar", font=("Arial", 12), bg="#191414", fg="white", command=get_top_tracks)
search_button.pack(pady=5)

# label nombre del artista
artist_label = tk.Label(root, text="", font=("Arial", 14, "bold italic"), bg="#1DB954", fg="white")
artist_label.pack(pady=5)

# mostrar canciones 
text_widget = tk.Text(root, width=35, height=20, font=("Arial", 12), bg="#FFFFFF", fg="#191414", wrap=tk.WORD)
text_widget.pack(pady=10)
text_widget.config(state=tk.DISABLED)

# correr la app
root.mainloop()
