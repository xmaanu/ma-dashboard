import duckdb

def crear_base_de_datos():
    # Conectamos con DuckDB y si el archivo no existe, lo crea automáticamente
    conn = duckdb.connect("deals.db")

    # Creamos la tabla donde guardaremos los deals
    # "IF NOT EXISTS" significa que si ya existe, no la borra ni da error
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id          VARCHAR,
            fecha       DATE,
            comprador   VARCHAR,
            comprada    VARCHAR,
            sector      VARCHAR,
            valor_musd  DOUBLE,
            descripcion VARCHAR
        )
    """)

    conn.close()
    print("Base de datos lista")

# Esto hace que si ejecutas este archivo directamente, cree la base de datos
if __name__ == "__main__":
    crear_base_de_datos()