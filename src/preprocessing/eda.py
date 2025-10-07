import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

DATA_DIR = "./data"
OUTPUT_DIR = "./reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set(style="whitegrid")

# ==============================
# FUNCIÓN DE ANÁLISIS
# ==============================

def generar_analisis_sensor(csv_path: str):
    """Genera un informe PDF con análisis exploratorio para un sensor."""

    nombre_sensor = os.path.splitext(os.path.basename(csv_path))[0]
    output_pdf = os.path.join(OUTPUT_DIR, f"{nombre_sensor}_analisis.pdf")

    # Cargar datos
    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"Archivo vacío: {csv_path}")
        return

    # Asegurar columnas esperadas
    columnas_requeridas = {"fecha", "hora", "decibelios"}
    if not columnas_requeridas.issubset(df.columns):
        print(f"Columnas faltantes en {csv_path}: {set(columnas_requeridas) - set(df.columns)}")
        return

    # Procesamiento de tiempo
    df["timestamp"] = pd.to_datetime(df["fecha"] + " " + df["hora"], errors="coerce")
    df = df.dropna(subset=["timestamp", "decibelios"])

    # Convertir decibelios a numérico
    df["decibelios"] = pd.to_numeric(df["decibelios"], errors="coerce")
    df = df.dropna(subset=["decibelios"])

    with PdfPages(output_pdf) as pdf:

        # 1. Resumen general
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis("off")
        resumen = df["decibelios"].describe().round(2).to_frame().T
        table = ax.table(
            cellText=resumen.values,
            colLabels=resumen.columns,
            rowLabels=resumen.index,
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        ax.set_title(f"Resumen estadístico - {nombre_sensor}", fontsize=16, weight="bold")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # 2. Evolución temporal
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=df, x="timestamp", y="decibelios", ax=ax, linewidth=0.6)
        ax.set_title("Evolución temporal del ruido", fontsize=14, weight="bold")
        ax.set_ylabel("Decibelios (dB)")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # 3. Distribución (Histograma + KDE)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df["decibelios"], bins=40, kde=True, ax=ax)
        ax.set_title("Distribución de niveles de ruido", fontsize=14, weight="bold")
        ax.set_xlabel("Decibelios (dB)")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # 4. Boxplot por mes
        df["mes"] = df["timestamp"].dt.to_period("M").astype(str)
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df, x="mes", y="decibelios", ax=ax)
        ax.set_title("Distribución mensual de decibelios", fontsize=14, weight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # 5. Boxplot por hora del día
        df["hora_num"] = pd.to_datetime(df["hora"], format="%H:%M", errors="coerce").dt.hour
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df, x="hora_num", y="decibelios", ax=ax)
        ax.set_title("Distribución horaria del ruido", fontsize=14, weight="bold")
        ax.set_xlabel("Hora del día")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        # 6. Promedio diario
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        daily_avg = df.groupby("fecha")["decibelios"].mean()
        fig, ax = plt.subplots(figsize=(12, 5))
        daily_avg.plot(ax=ax)
        ax.set_title("Promedio diario de ruido", fontsize=14, weight="bold")
        ax.set_ylabel("Decibelios (dB)")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

    print(f"Análisis generado: {output_pdf}")


# ==============================
# PROCESAR TODOS LOS ARCHIVOS
# ==============================

def main():
    archivos_csv = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

    if not archivos_csv:
        print("No se encontraron archivos CSV en la carpeta data.")
        return

    for csv_path in archivos_csv:
        try:
            generar_analisis_sensor(csv_path)
        except Exception as e:
            print(f"Error procesando {csv_path}: {e}")


if __name__ == "__main__":
    main()
