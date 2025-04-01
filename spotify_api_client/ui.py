import tkinter as tk
from tkinter import messagebox
from app import get_top_tracks  # Importa la función del backend

# función para manejar la búsqueda
def search_tracks():
    artist_name = entry.get().strip()
    artist, songs = get_top_tracks(artist_name)

    if not artist:
        messagebox.showerror("Error", songs)
        return
    
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    artist_label.config(text=f"🎵 {artist} - Top 10 🎵")  

    for idx, song in enumerate(songs, start=1):
        text_widget.insert(tk.END, f"{idx}. {song}\n\n")

    text_widget.config(state=tk.DISABLED)
    entry.delete(0, tk.END)  # Limpiar campo de entrada

# ventana principal
root = tk.Tk()
root.title("Spotify Web API")
root.geometry("350x600")
root.resizable(False, False)
root.configure(bg="#1DB954")

# frame para centrar los elementos
frame = tk.Frame(root, bg="#1DB954")
frame.pack(pady=20)

# titulo
title_label = tk.Label(frame, text="Top 10 Canciones", font=("Arial", 16, "bold"), bg="#1DB954", fg="white")
title_label.pack()

# barra de búsqueda
entry = tk.Entry(frame, width=20, font=("Arial", 14), justify='center')
entry.pack(pady=10)

# botón buscar
search_button = tk.Button(frame, text="Buscar", font=("Arial", 12), bg="#191414", fg="white", command=search_tracks)
search_button.pack(pady=5)

# label para el nombre del artista
artist_label = tk.Label(root, text="", font=("Arial", 14, "bold italic"), bg="#1DB954", fg="white")
artist_label.pack(pady=5)

# mostrar canciones 
text_widget = tk.Text(root, width=35, height=20, font=("Arial", 12), bg="#FFFFFF", fg="#191414", wrap=tk.WORD)
text_widget.pack(pady=10)
text_widget.config(state=tk.DISABLED)

# correr la app
root.mainloop()
