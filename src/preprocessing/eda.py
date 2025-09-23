import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Ruta de datos
DATA_FILE = "ruido_cuenca.csv"
OUTPUT_PDF = "analisis_exploratorio.pdf"

# Cargar datos
df = pd.read_csv(DATA_FILE)

# Parsear timestamp
df["timestamp"] = pd.to_datetime(df["fecha"] + " " + df["hora"], errors="coerce")

# Configuración estética
sns.set(style="whitegrid")

with PdfPages(OUTPUT_PDF) as pdf:

    # --- 1. Resumen general ---
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    resumen = df["decibelios"].describe().round(2).to_frame().T
    table = ax.table(cellText=resumen.values,
                     colLabels=resumen.columns,
                     rowLabels=resumen.index,
                     loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    ax.set_title("Resumen estadístico de los decibelios", fontsize=16, weight="bold")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # --- 2. Evolución temporal ---
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x="timestamp", y="decibelios", ax=ax, linewidth=0.6)
    ax.set_title("Evolución temporal del ruido", fontsize=14, weight="bold")
    ax.set_ylabel("Decibelios (dB)")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # --- 3. Distribución (Histograma + KDE) ---
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["decibelios"].dropna(), bins=40, kde=True, ax=ax)
    ax.set_title("Distribución de niveles de ruido", fontsize=14, weight="bold")
    ax.set_xlabel("Decibelios (dB)")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # --- 4. Boxplot por mes (para detectar outliers) ---
    df["mes"] = df["timestamp"].dt.to_period("M").astype(str)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df, x="mes", y="decibelios", ax=ax)
    ax.set_title("Distribución de decibelios por mes", fontsize=14, weight="bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # --- 5. Boxplot por hora (para ruido típico en el día) ---
    df["hora_num"] = pd.to_datetime(df["hora"], format="%H:%M", errors="coerce").dt.hour
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df, x="hora_num", y="decibelios", ax=ax)
    ax.set_title("Distribución de decibelios por hora del día", fontsize=14, weight="bold")
    ax.set_xlabel("Hora del día")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # --- 6. Promedio diario ---
    df["fecha"] = pd.to_datetime(df["fecha"])
    daily_avg = df.groupby("fecha")["decibelios"].mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    daily_avg.plot(ax=ax)
    ax.set_title("Promedio diario de ruido", fontsize=14, weight="bold")
    ax.set_ylabel("Decibelios (dB)")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

print(f"✅ Análisis exploratorio guardado en {OUTPUT_PDF}")
