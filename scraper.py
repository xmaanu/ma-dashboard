import requests
import pandas as pd
import duckdb
from datetime import datetime, timedelta

# Cabeceras que exige la API de EDGAR para identificar quién hace la petición
HEADERS = {
    "User-Agent": "ma-dashboard camposfdezmanuel@gmail.com"
}

def obtener_deals_recientes():
    """Pide a EDGAR los filings de tipo 8-K de los últimos 30 días"""
    
    # Fecha de hoy y hace 30 días
    hoy = datetime.today()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Petición a la API de EDGAR
    # todo lo que hay despues de ? son los filtros de busqueda que queremos, en este caso M&A
    # forms=8-K filtra solo los formularios de 8-K (urgentes)
    #dateRange=... filtra por rango de fechas
    url = "https://efts.sec.gov/LATEST/search-index?q=%22merger%22+%22acquisition%22&dateRange=custom&startdt={}&enddt={}&forms=8-K".format(
        hace_30_dias.strftime("%Y-%m-%d"),
        hoy.strftime("%Y-%m-%d")
    )
    
    print("Pidiendo datos a EDGAR...")
    respuesta = requests.get(url, headers=HEADERS)
    
    # Comprobamos que la petición ha ido bien
    if respuesta.status_code != 200:
        print("Error al conectar con EDGAR:", respuesta.status_code)
        return []
    
    #recibimos los datos en json y dentro de este cogemos la lista de hits
    datos = respuesta.json()
    filings = datos.get("hits", {}).get("hits", [])
    print(f"Encontrados {len(filings)} filings")
    
    return filings

def limpiar_nombre(nombre_raw):
    """Extrae solo el nombre limpio de la cadena que devuelve EDGAR"""
    if not nombre_raw:
        return ""
    # Convertimos a string por si viene como lista
    texto = str(nombre_raw)
    # Cogemos solo lo que hay antes del primer paréntesis
    nombre = texto.split("(")[0]
    # Quitamos caracteres sobrantes
    nombre = nombre.replace("[", "").replace("]", "").replace("'", "").strip()
    return nombre

def procesar_filings(filings):
    """Extrae la información relevante de cada filing"""
    
    deals = []
    
    for filing in filings:
        fuente = filing.get("_source", {})
        
        deal = {
            "id":          fuente.get("file_num", ""),
            "fecha":       fuente.get("file_date") or None,
            "comprador": limpiar_nombre(fuente.get("display_names", "")),
            "comprada":    "",
            "sector":      fuente.get("form_type", ""),
            "valor_musd":  None,
            "descripcion": fuente.get("entity_name", "")
        }
        
        deals.append(deal)
    
    return deals

def guardar_en_base_de_datos(deals):
    """Guarda los deals en DuckDB evitando duplicados"""
    
    if not deals:
        print("No hay deals que guardar")
        return
    
    conn = duckdb.connect("deals.db")
    
    guardados = 0
    for deal in deals:
        # Comprobamos si este deal ya existe por su id
        existe = conn.execute(
            "SELECT COUNT(*) FROM deals WHERE id = ?", [deal["id"]]
        ).fetchone()[0]
        
        if not existe:
            conn.execute("""
                INSERT INTO deals VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                deal["id"],
                deal["fecha"],
                deal["comprador"],
                deal["comprada"],
                deal["sector"],
                deal["valor_musd"],
                deal["descripcion"]
            ])
            guardados += 1
    
    conn.close()
    print(f"Guardados {guardados} deals nuevos")

def ejecutar_scraper():
    """Función principal que une todo"""
    from database import crear_base_de_datos
    
    crear_base_de_datos()
    filings = obtener_deals_recientes()
    deals = procesar_filings(filings)
    guardar_en_base_de_datos(deals)

if __name__ == "__main__":
    ejecutar_scraper()