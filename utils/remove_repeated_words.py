import json
import sys
import os

def eliminar_repetidos_por_clave(ruta_json):
    if not os.path.isfile(ruta_json):
        print(f"Error: el archivo '{ruta_json}' no existe.")
        return

    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        print("Error: el JSON debe ser un diccionario clave:valor.")
        return

    seen_keys = set()
    data_sin_repetidos = {}
    eliminados = []

    for key, value in data.items():
        key_norm = key.strip().lower()
        if key_norm not in seen_keys:
            data_sin_repetidos[key] = value
            seen_keys.add(key_norm)
        else:
            eliminados.append((key, value))

    ruta_salida = f"{os.path.splitext(ruta_json)[0]}.json"
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(data_sin_repetidos, f, ensure_ascii=False, indent=2)

    print(f"JSON sin claves repetidas creado correctamente: {ruta_salida}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python remove_repeated_words.py r   zzzuta_del_json.json")
    else:
        eliminar_repetidos_por_clave(sys.argv[1])
