# Predicción de Contaminación Sónica en Cuenca 🇪🇨

Este proyecto tiene como objetivo **predecir los niveles de contaminación acústica en la ciudad de Cuenca (Ecuador)** aplicando un enfoque de **aprendizaje profundo espacio–temporal**.  

La implementación se adapta a las condiciones locales: en Cuenca se cuenta con **9 puntos de monitoreo continuo** que actúan como nodos en el grafo urbano.

---

## 📌 Objetivos

- **Recolectar datos acústicos** automáticamente desde fuentes públicas mediante técnicas de **web scraping** en Python.  
- **Construir un dataset espacio–temporal** con registros de los 9 puntos de monitoreo.  
- **Realizar análisis estadístico exploratorio** de los niveles de ruido (distribuciones, tendencias, correlaciones).  
- **Desarrollar un modelo híbrido** que combine dependencias temporales y espaciales para predecir la evolución del ruido.  

---

## 🗂️ Estructura del proyecto

```
├── data/                # Datos crudos y procesados
├── notebooks/           # Jupyter notebooks de análisis estadístico
├── src/
│   ├── scraping/        # Scripts de web scraping
│   ├── preprocessing/   # Limpieza y preparación de datos
│   ├── models/          # Definición y entrenamiento de modelos
│   └── utils/           # Funciones auxiliares
├── README.md            # Descripción del proyecto
└── requirements.txt     # Dependencias de Python
```

---

## 🔧 Tecnologías principales

- **Python 3.10+**  
- Librerías para scraping: `requests`, `BeautifulSoup`, `selenium`  
- Librerías de análisis y modelado: `pandas`, `numpy`, `scikit-learn`, `torch`  
- Visualización: `matplotlib`, `seaborn`  

---

## 📊 Metodología

1. **Extracción de datos** mediante web scraping de registros de ruido en los 9 nodos de Cuenca.  
2. **Procesamiento y normalización** de series día/noche en decibeles (dBA).  
3. **Construcción del grafo espacial**:  
   - Cada estación = nodo.  
   - Conexión con sus vecinos más cercanos según distancia geográfica (Haversine).  
4. **Entrenamiento del modelo híbrido**:  
   - CNN1D para patrones locales en el tiempo.  
   - LSTM para dependencias de largo plazo.  
   - TransformerConv para difusión espacial con atención.  
5. **Evaluación con métricas estándar**: RMSE, MAE, R², correlación y accuracy.  

---

## 🚀 Uso

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/aristring/ruido-cuenca.git
   cd nombre_repositorio
   ```

2. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar el scraping:  
   ```bash
   python src/scraping/run_scraper.py
   ```

4. Analizar los datos en `notebooks/` o entrenar el modelo con:  
   ```bash
   python src/models/train.py
   ```
