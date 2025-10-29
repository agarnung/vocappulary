# Para crear el ejecutable:
# Asegúrate de tener Python instalado (ya sea en Windows o Unix)
#   $ python3 -m venv vocappulary_venv
#   $ source vocappulary_venv/bin/activate # o .\vocappulary_venv\Scripts\Activate.ps1 en Windows
#   Opcion 1: local
#       pip install -r requirements.txt
#       python main.py
#   Opcion 2: ejecutable (se generará el nativo de la máquina que ejecute el comando)
#       $ pip install pyinstaller
#       $ pyinstaller --onefile --noconsole --name=Vocappulary main.py
#       La app estará disponible en /mnt/c/Users/Alejandro/Documents/proyectos/vocappulary/dist
#       Copia la app a donde estén los .json con los diccionarios 
# Troubleshooting:
# Si lo ejecutas desde le WSL y da proplemas al instalar, asegúrate de añadir nameserver 8.8.8.8 a /etc/resolv.conf,
# ver https://stackoverflow.com/questions/52815784/python-pip-raising-newconnectionerror-while-installing-libraries

import tkinter as tk
from tkinter import messagebox
import json, random, unicodedata, os
import time

# Funciones auxiliares
def quitar_tildes(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def comparar_respuestas(resp, correcta):
    """Devuelve: 'ok', 'tilde', o 'mal'"""
    if resp == correcta:
        return "ok"
    elif quitar_tildes(resp) == quitar_tildes(correcta):
        return "tilde"
    else:
        return "mal"

# Lógica principal
class VocabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulario 🇫🇷 🇬🇧 -> 🇪🇸")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        # Color de fondo de la ventana
        self.root.config(bg="#f0f4f8") # azul claro

        self.idioma = tk.StringVar(value="fr")
        self.modo = tk.StringVar(value="a_es")

        self.palabras = {}
        self.palabras_lista = []
        self.indice = 0

        self.crear_menu_inicial()

    def crear_menu_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root, text="Elige idioma:", font=("Arial", 14), bg="#f0f4f8"
        ).pack(pady=10)
        tk.Radiobutton(
            self.root, text="Francés", font=("Arial", 12), variable=self.idioma, value="fr", bg="#f0f4f8"
        ).pack()
        tk.Radiobutton(
            self.root, text="Inglés", font=("Arial", 12), variable=self.idioma, value="en", bg="#f0f4f8"
        ).pack()

        tk.Label(
            self.root, text="Modo:", font=("Arial", 14), bg="#f0f4f8"
        ).pack(pady=10)
        tk.Radiobutton(
            self.root, text="Traducir al español", font=("Arial", 12), variable=self.modo, value="a_es", bg="#f0f4f8"
        ).pack()
        tk.Radiobutton(
            self.root, text="Traducir al idioma", font=("Arial", 12), variable=self.modo, value="a_idioma", bg="#f0f4f8"
        ).pack()

        tk.Button(
            self.root,
            text="Comenzar",
            command=self.iniciar,
            font=("Arial", 14, "bold"),
            bg="#4e73df", # azul 
            fg="white",
            activebackground="#2e59d9",
            activeforeground="white",
            relief="raised",
            bd=3,
        ).pack(pady=20)

    def iniciar(self):
        archivo = "palabras_fr.json" if self.idioma.get() == "fr" else "palabras_en.json"
        with open(archivo, "r", encoding="utf-8") as f:
            self.palabras = json.load(f)

        self.palabras_lista = list(self.palabras.keys())
        random.shuffle(self.palabras_lista)
        self.indice = 0
        self.crear_interfaz_juego()
        self.nueva_palabra()

    def crear_interfaz_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label_palabra = tk.Label(self.root, text="", font=("Arial", 24, "bold"))
        self.label_palabra.pack(pady=20)

        self.entrada = tk.Entry(self.root, font=("Arial", 16))
        self.entrada.pack(pady=10)
        self.entrada.bind("<Return>", lambda e: self.comprobar())

        self.boton = tk.Button(self.root, text="Comprobar", command=self.comprobar, font=("Arial", 14))
        self.boton.pack(pady=10)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)


    def nueva_palabra(self):
        # Re-hash según hora actual para más aleatoriedad
        seed = int(time.time() * 1000) % 9999999 # ms
        random.seed(seed)
        palabra = random.choice(self.palabras_lista) # Siempre puede repetirse

        if self.modo.get() == "a_es":
            texto = palabra
        else:
            texto = self.palabras[palabra]

        self.palabra_actual = palabra
        self.label_palabra.config(text=texto)
        self.entrada.delete(0, tk.END)
        self.info_label.config(text="")

    def comprobar(self):
        palabra = self.palabra_actual
        respuesta = self.entrada.get().strip().lower()

        if self.modo.get() == "a_es":
            correcta = self.palabras[palabra].lower()
        else:
            correcta = palabra.lower()

        resultado = comparar_respuestas(respuesta, correcta)

        if resultado == "ok":
            self.info_label.config(
                text=f"✅ Correcto: {correcta}",
                fg="#28a745", # verde 
                font=("Arial", 12, "bold")
            )
            self.root.after(800, self.nueva_palabra)
        elif resultado == "tilde":
            self.info_label.config(
                text=f"🟧 Casi correcto\nEra: {correcta}",
                fg="#fd7e14", # naranja
                font=("Arial", 12, "bold")
            )
            self.root.after(1200, self.nueva_palabra)
        else:
            self.info_label.config(
                text=f"❌ Incorrecto\nEra: {correcta}",
                fg="#dc3545", # rojo
                font=("Arial", 12, "bold")
            )
            self.root.after(1000, self.nueva_palabra)

# Inicio del programa
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x300")
    root.resizable(False, False)
    icono = tk.PhotoImage(file="favicon.png")
    root.iconphoto(True, icono)
    app = VocabApp(root)
    root.mainloop()
