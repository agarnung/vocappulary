# Vocappulary

App de escritorio para **practicar vocabulario** en Francés **🇫🇷** e Inglés **🇬🇧** a Español **🇪🇸**

Aprox. **> 1300 términos** y en crecimiento.

## Cómo funciona

* Elegir idioma de origen (Francés o Inglés)
* Elegir modo: traducir al español o al idioma original
* Introducir la traducción en la entrada de texto y pulsar **Enter** o **Comprobar**
* La app indicará si la respuesta es correcta, casi correcta (solo tilde) o incorrecta

### Mensajes

* ✅ Correcto
* 🟧 Casi correcto (e.g. fallo en tilde)
* ❌ Incorrecto (se muestra la respuesta correcta tras un salto de línea)

## Para usuarios

[Descarga el ZIP](https://github.com/agarnung/vocappulary/releases/download/v1.0/vocappulary.zip), descomprímelo en `C:\Archivos de Programa` (o donde quieras) y haz doble click en el **.exe**, o en un acceso al escritorio. 

¡Y empieza a aprender idiomas a base de fuerza bruta!.

## Para desarrolladores

### Requisitos

- Python 3.x
- Tkinter (viene con Python)
- Instalar dependencias:  
```bash
pip install -r requirements.txt
```

### Opción 1: Ejecutar localmente

```bash
python3 -m venv vocappulary_venv
source vocappulary_venv/bin/activate # Linux / macOS
# .\vocappulary_venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
python3 main.py
```

### Opción 2: Generar ejecutable

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name=Vocappulary main.py
```

El ejecutable se encontrará en `dist/Vocappulary.exe`. Copiarlo al directorio donde están los diccionarios `.json`.

### Archivos principales

* `main.py` → Script principal de la app.
* `palabras_fr.json` / `palabras_en.json` → Diccionarios de vocabulario.
* `favicon.png` → Icono de la ventana.

### Troubleshooting

Si hay problemas de red en WSL al instalar librerías, añadir `nameserver 8.8.8.8` a `/etc/resolv.conf`.

Ver [StackOverflow](https://stackoverflow.com/questions/52815784/python-pip-raising-newconnectionerror-while-installing-libraries).

## Utils incluidos

### 1. Eliminar palabras repetidas
```bash
python remove_repeated_words.py ruta_del_json.json
```

* Elimina claves repetidas de un JSON.
* Nota: JSON no permite claves duplicadas. Este script elimina duplicados del propio archivo de texto pero no estarían en memoria después de cargar el JSON.

### 2. Traducir vocabulario automáticamente

```bash
python translate_json.py [en-fr|fr-en] ruta_del_json.json
```

* `en-fr` → Traduce de inglés a francés.
* `fr-en` → Traduce de francés a inglés.
* Mantiene los valores en español.
* Genera un nuevo archivo con sufijo `_fr` o `_en` según el modo.
* La librería puede fallar en ciertos escenarios; no estamos usando token por ahora.
