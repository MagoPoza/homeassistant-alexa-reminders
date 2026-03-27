#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime, timedelta

NEW_FILE = "/config/www/recordatorios/alexa_reminders_new.json"
OLD_FILE = "/config/www/recordatorios/alexa_reminders_old.json"

def load_json(filename):
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

nuevos = load_json(NEW_FILE)
antiguos = load_json(OLD_FILE)

if not isinstance(nuevos, list):
    nuevos = []
if not isinstance(antiguos, list):
    antiguos = []

# Usar el id de Amazon como identificador único
antiguos_ids = {r.get('id', '') for r in antiguos if r.get('id')}

nuevos_eventos = []
for rec in nuevos:
    rec_id = rec.get('id', '')
    if not rec_id or rec_id in antiguos_ids:
        continue
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

sys.stdout.write(json.dumps(nuevos_eventos))
sys.stdout.flush()
