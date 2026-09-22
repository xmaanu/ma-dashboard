# M&A Deal Explorer

🔗 Demo en vivo: https://ma-dashboard-2.streamlit.app/

Dashboard interactivo que extrae y visualiza operaciones de fusiones y adquisiciones (M&A) de empresas cotizadas en Estados Unidos, usando datos públicos de la SEC (Securities and Exchange Commission).

## ¿Qué problema resuelve?

La base de datos pública de la SEC (EDGAR) contiene miles de documentos sobre operaciones de M&A, pero son difíciles de explorar y analizar en bruto. Este proyecto automatiza la extracción de esos datos y los presenta en un dashboard visual e interactivo.

## Tecnologías utilizadas

- Python — lenguaje principal
- SEC EDGAR API — fuente de datos pública y gratuita
- pandas — limpieza y manipulación de datos
- DuckDB — base de datos local ligera
- Streamlit — dashboard interactivo
- Plotly — visualización de datos

## Cómo ejecutarlo

1. Clona el repositorio
2. Instala las dependencias:

pip install requests pandas duckdb streamlit plotly

3. Descarga los datos de EDGAR:

python scraper.py

4. Lanza el dashboard:

streamlit run dashboard.py

5. Abre tu navegador en http://localhost:8501

## Funcionalidades

- Extracción automática de filings 8-K relacionados con M&A de los últimos 30 días
- Filtro interactivo por rango de fechas
- Métricas generales: total de deals, actividad semanal y empresas únicas
- Gráfico de actividad por fecha
- Tabla de deals ordenada por fecha

## Actualización de datos

La versión desplegada en Streamlit Cloud obtiene datos frescos de SEC EDGAR 
automáticamente cada vez que se abre el dashboard.

Si ejecutas el proyecto en local, actualiza los datos manualmente con:

    python scraper.py

## Posibles mejoras futuras

- Añadir formularios SC 13D y SC TO-T además de los 8-K
- Incorporar clasificación automática por sector
- Implementar actualización automática diaria de los datos
- Añadir análisis de sentimiento sobre los textos de los filings
