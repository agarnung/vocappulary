import json
from googletrans import Translator
import sys
import os

def traducir_json(modo, ruta_json):
    if not os.path.isfile(ruta_json):
        print(f"Error: el archivo '{ruta_json}' no existe.")
        return

    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    translator = Translator()
    resultado = {}

    carpeta = os.path.dirname(ruta_json) 
    if modo == "en-fr":
        src, dest = "en", "fr"
        ruta_salida = os.path.join(carpeta, "palabras_fr.json")
    elif modo == "fr-en":
        src, dest = "fr", "en"
        ruta_salida = os.path.join(carpeta, "palabras_en.json")
    else:
        print("Modo inválido. Usa 'en-fr' o 'fr-en'.")
        return

    for word, es_word in data.items():
        traduccion = translator.translate(word, src=src, dest=dest).text
        resultado[traduccion] = es_word

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"JSON traducido creado correctamente: {ruta_salida}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python translate_json.py [en-fr|fr-en] ruta_del_json.json")
    else:
        modo = sys.argv[1]
        ruta_json = sys.argv[2]
        traducir_json(modo, ruta_json)
