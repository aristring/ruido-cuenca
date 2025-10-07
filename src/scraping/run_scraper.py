import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
BASE_URL = "https://ierse.uazuay.edu.ec/proyectos/ruido-continuo/lib/getinfo_areachartfix.php"

# Lista de sensores (idw)
SENSORES = [
    {"idw": "SCP01", "mx7": 55, "mx21": 45},
    {"idw": "SCP06", "mx7": 60, "mx21": 50},
    {"idw": "SCP07", "mx7": 60, "mx21": 50},
    {"idw": "SCP08", "mx7": 60, "mx21": 50},
    {"idw": "SCP09", "mx7": 70, "mx21": 65},
    {"idw": "SCP13", "mx7": 55, "mx21": 45},
    {"idw": "SCP16", "mx7": 55, "mx21": 45},
    {"idw": "SCP17", "mx7": 55, "mx21": 45}
]

# Carpeta de salida
OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Rango de fechas: últimos 365 días
end_date = datetime.today()
start_date = end_date - timedelta(days=365)
total_days = (end_date - start_date).days + 1

# ==============================
# DESCARGA DE DATOS
# ==============================
start_time = time.time()

for sensor in SENSORES:
    idw = sensor["idw"]
    mx7 = sensor["mx7"]
    mx21 = sensor["mx21"]

    print(f"\nDescargando datos para sensor {idw}...")
    all_data = []

    current_date = start_date
    for _ in tqdm(range(total_days), desc=f"{idw}", unit="día"):
        fecha_str = current_date.strftime("%Y-%m-%d")
        url = f"{BASE_URL}?idw={idw}&fch={fecha_str}&mx7={mx7}&mx21={mx21}"

        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()

            text = resp.text.strip()
            if not text or text == "[]":
                current_date += timedelta(days=1)
                continue

            text = text.replace("null", "None")
            try:
                data = eval(text)
            except Exception:
                current_date += timedelta(days=1)
                continue

            for row in data:
                if len(row) >= 2:
                    hora = row[0]
                    val = row[1]
                    if val is not None:
                        all_data.append({
                            "sensor": idw,
                            "fecha": fecha_str,
                            "hora": hora,
                            "decibelios": val
                        })

        except Exception as e:
            print(f"Error con {idw} ({fecha_str}): {e}")

        time.sleep(0.3)
        current_date += timedelta(days=1)

    # ==============================
    # GUARDAR ARCHIVO CSV
    # ==============================
    if all_data:
        df = pd.DataFrame(all_data)
        output_path = os.path.join(OUTPUT_DIR, f"ruido_{idw}.csv")
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Datos guardados en {output_path}")
    else:
        print(f"No se obtuvieron datos para el sensor {idw}.")

# ==============================
# TIEMPO TOTAL
# ==============================
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTiempo total: {elapsed_time:.2f} segundos")
print(f"Archivos guardados en: {os.path.abspath(OUTPUT_DIR)}")
