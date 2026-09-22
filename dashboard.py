import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

def cargar_datos():
    import os
    # Si existe la base de datos local, la usamos (desarrollo en el ordenador)
    if os.path.exists("deals.db"):
        conn = duckdb.connect("deals.db")
        df = conn.execute("SELECT * FROM deals").df()
        conn.close()
        return df
    # Si no existe (Streamlit Cloud), pedimos los datos directamente a EDGAR
    else:
        from scraper import obtener_deals_recientes, procesar_filings
        filings = obtener_deals_recientes()
        deals = procesar_filings(filings)
        return pd.DataFrame(deals)

# Configuración de la página
st.set_page_config(
    page_title="M&A Deal Explorer",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 M&A Deal Explorer")
st.caption("Datos extraídos de SEC EDGAR en tiempo real")

# Cargamos los datos
df = cargar_datos()

# --- FILTROS ---
st.sidebar.header("Filtros")

# Filtro por fecha
fecha_min = df["fecha"].min()
fecha_max = df["fecha"].max()

fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Rango de fechas",
    value=[fecha_min, fecha_max],
    min_value=fecha_min,
    max_value=fecha_max
)

# Aplicamos el filtro
df_filtrado = df[
    (df["fecha"] >= pd.Timestamp(fecha_inicio)) &
    (df["fecha"] <= pd.Timestamp(fecha_fin))
]

# --- MÉTRICAS GENERALES ---
st.subheader("Resumen")
col1, col2, col3 = st.columns(3)

col1.metric("Total de deals", len(df_filtrado))
col2.metric("Deals esta semana", len(df_filtrado[df_filtrado["fecha"] >= pd.Timestamp("today") - pd.Timedelta(days=7)]))
col3.metric("Empresas únicas", df_filtrado["comprador"].nunique())

# --- GRÁFICO DE ACTIVIDAD ---
st.subheader("Actividad por fecha")

actividad = df_filtrado.groupby("fecha").size().reset_index(name="deals")
fig = px.bar(actividad, x="fecha", y="deals", labels={"fecha": "Fecha", "deals": "Número de deals"})
st.plotly_chart(fig, use_container_width=True)

# --- TABLA DE DEALS ---
st.subheader("Deals recientes")

st.dataframe(
    df_filtrado[["fecha", "comprador", "sector", "valor_musd"]].sort_values("fecha", ascending=False),
    use_container_width=True
)