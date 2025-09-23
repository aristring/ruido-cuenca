import requests
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import time

# Medir tiempo total
start_time = time.time()

# Parámetros base
base_url = "https://ierse.uazuay.edu.ec/proyectos/ruido-continuo/lib/getinfo_areachartfix.php"
idw = "SCP01"  # puedes cambiarlo por otro nodo si deseas
mx7 = 55
mx21 = 45

# Rango de fechas: último año
end_date = datetime.today()
start_date = end_date - timedelta(days=365)
total_days = (end_date - start_date).days + 1

# Lista para acumular datos
all_data = []

# Iterar día por día con barra de progreso
current_date = start_date
for _ in tqdm(range(total_days), desc="Descargando datos", unit="día"):
    fecha_str = current_date.strftime("%Y-%m-%d")  # ejemplo: 2025-09-20
    url = f"{base_url}?idw={idw}&fch={fecha_str}&mx7={mx7}&mx21={mx21}"

    try:
        resp = requests.get(url)
        resp.raise_for_status()

        # El resultado es un array JS (ej: [['00:02', null,45], ...])
        text = resp.text.strip()
        text = text.replace("null", "None")  # Python entiende None
        data = eval(text)  # convierte string en lista

        for row in data:
            hora = row[0]
            val1 = row[1]  # medición real

            # Solo guardar si hay valor real
            if val1 is not None:
                all_data.append({
                    "fecha": fecha_str,
                    "hora": hora,
                    "decibelios": val1
                })

    except Exception as e:
        print(f"Error con fecha {fecha_str}: {e}")

    current_date += timedelta(days=1)

# Convertir a DataFrame
df = pd.DataFrame(all_data)

# Guardar en CSV
df.to_csv("ruido_cuenca.csv", index=False, encoding="utf-8")

# Medir tiempo final
end_time = time.time()
elapsed_time = end_time - start_time
print(f"✅ Datos guardados en ruido_cuenca.csv")
print(f"⏱️ Tiempo total: {elapsed_time:.2f} segundos")
