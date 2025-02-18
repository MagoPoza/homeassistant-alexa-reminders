#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime, timedelta

# Rutas de los archivos JSON (ajusta según tu configuración)
NEW_FILE = "/config/www/recordatorios/alexa_reminders_new.json"
OLD_FILE = "/config/www/recordatorios/alexa_reminders_old.json"

def load_json(filename):
    """Carga un archivo JSON y devuelve una lista. Si el archivo no existe o está corrupto, devuelve []"""
    try:
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error leyendo {filename}: archivo no es un JSON válido")
        return []
    except Exception as e:
        print(f"Error leyendo {filename}: {e}")
        return []

def save_json(filename, data):
    """Guarda datos en un archivo JSON"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error escribiendo {filename}: {e}")

# Cargar datos de los archivos
nuevos = load_json(NEW_FILE)
antiguos = load_json(OLD_FILE)

# Verificar que sean listas válidas
if not isinstance(nuevos, list):
    nuevos = []
if not isinstance(antiguos, list):
    antiguos = []

# Función para identificar un recordatorio de manera única
def identifier(rec):
    return f"{rec.get('recordatorio', '')}_{rec.get('fecha', '')}_{rec.get('hora', '')}_{rec.get('persona', '')}"

# Generar sets para comparación
antiguos_ids = {identifier(r) for r in antiguos}

# Lista de eventos nuevos
nuevos_eventos = []

for rec in nuevos:
    if identifier(rec) not in antiguos_ids:
        try:
            start_dt = datetime.strptime(f"{rec['fecha']} {rec['hora']}", "%Y-%m-%d %H:%M:%S")
            end_dt = start_dt + timedelta(minutes=1)

            event_data = {
                "summary": rec["recordatorio"],
                "start_date_time": start_dt.isoformat(),
                "end_date_time": end_dt.isoformat(),
                "persona": rec["persona"]
            }

            nuevos_eventos.append(event_data)
        except Exception as e:
            print(f"Error procesando recordatorio {rec}: {e}")


# Devolver salida JSON válida para Home Assistant
sys.stdout.write(json.dumps(nuevos_eventos))
sys.stdout.flush()
