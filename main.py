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

def comparar_respuestas(resp, lista_correctas):
    """Devuelve: 'ok', 'tilde', o 'mal'"""
    # Normalizar la respuesta del usuario
    resp_normalizada = resp.lower().strip()
    resp_sin_tildes = quitar_tildes(resp_normalizada)
    
    # Verificar si coincide exactamente con alguna opción
    for correcta in lista_correctas:
        if resp_normalizada == correcta.lower():
            return "ok", correcta  # Devolver también la opción que coincidió
    
    # Verificar si coincide sin tildes
    for correcta in lista_correctas:
        if resp_sin_tildes == quitar_tildes(correcta.lower()):
            return "tilde", correcta  # Devolver también la opción que coincidió
    
    return "mal", None

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
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                self.palabras = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {archivo}")
            return

        self.palabras_lista = list(self.palabras.keys())
        random.shuffle(self.palabras_lista)
        self.indice = 0
        self.crear_interfaz_juego()
        self.nueva_palabra()

    def crear_interfaz_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal para palabra y entrada
        self.frame_central = tk.Frame(self.root, bg="#f0f4f8")
        self.frame_central.pack(expand=True, fill="both", pady=(20,10))

        self.label_palabra = tk.Label(self.frame_central, text="", font=("Arial", 24, "bold"), bg="#f0f4f8")
        self.label_palabra.pack(pady=10)

        self.entrada = tk.Entry(self.frame_central, font=("Arial", 16))
        self.entrada.pack(pady=5)
        self.entrada.bind("<Return>", lambda e: self.comprobar())
        self.entrada.focus() # Poner foco en la entrada

        self.boton = tk.Button(self.frame_central, text="Comprobar", command=self.comprobar, font=("Arial", 14))
        self.boton.pack(pady=5)

        self.info_label = tk.Label(self.frame_central, text="", font=("Arial", 12), bg="#f0f4f8")
        self.info_label.pack(pady=(10, 5))

        # Frame fijo para el botón de volver
        self.frame_footer = tk.Frame(self.root, bg="#f0f4f8")
        self.frame_footer.pack(side="bottom", fill="x", pady=(0, 25))

        self.volver_btn = tk.Button(
            self.frame_footer,
            text="⬅ Volver",
            command=self.crear_menu_inicial,
            font=("Arial", 12),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white"
        )
        self.volver_btn.pack()

    def nueva_palabra(self):
        if not self.palabras_lista:
            messagebox.showinfo("Fin", "¡Has completado todas las palabras!")
            self.crear_menu_inicial()
            return

        palabra = random.choice(self.palabras_lista)

        if self.modo.get() == "a_es":
            texto = palabra
        else:
            opciones_espanol = self.palabras[palabra]
            texto = random.choice(opciones_espanol)

        self.palabra_actual = palabra
        self.label_palabra.config(text=texto)
        self.entrada.delete(0, tk.END)
        self.info_label.config(text="")
        self.entrada.focus() # Volver a poner foco en la entrada

    def comprobar(self):
        palabra = self.palabra_actual
        respuesta = self.entrada.get().strip()

        if not respuesta:
            self.info_label.config(
                text="⚠️ Por favor, ingresa una respuesta",
                fg="#ffc107", # amarillo
                font=("Arial", 12, "bold")
            )
            return

        if self.modo.get() == "a_es":
            opciones_correctas = self.palabras[palabra]
            resultado, opcion_coincidente = comparar_respuestas(respuesta, opciones_correctas)
            
            if resultado == "ok":
                correcta_mostrar = respuesta 
            else:
                correcta_mostrar = random.choice(opciones_correctas)
        else:
            opciones_correctas = [palabra] 
            resultado, opcion_coincidente = comparar_respuestas(respuesta, opciones_correctas)
            correcta_mostrar = palabra

        if resultado == "ok":
            self.info_label.config(
                text=f"✅ Correcto: {correcta_mostrar}",
                fg="#28a745", # verde 
                font=("Arial", 12, "bold")
            )
            self.root.after(750, self.nueva_palabra)
        elif resultado == "tilde":
            self.info_label.config(
                text=f"🟧 Casi correcto\nEra: {correcta_mostrar}",
                fg="#fd7e14", # naranja
                font=("Arial", 12, "bold")
            )
            self.root.after(1500, self.nueva_palabra)
        else:
            self.info_label.config(
                text=f"❌ Incorrecto\nEra: {correcta_mostrar}",
                fg="#dc3545", # rojo
                font=("Arial", 12, "bold")
            )
            self.root.after(1750, self.nueva_palabra)

# Inicio del programa
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x300")
    root.resizable(False, False)
    try:
        icono = tk.PhotoImage(file="favicon.png")
        root.iconphoto(True, icono)
    except:
        pass 
    app = VocabApp(root)
    root.mainloop()