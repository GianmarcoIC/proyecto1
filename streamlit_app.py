# streamlit_app.py
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar variables de entorno (si se usan .env)
load_dotenv()

# Configurar la conexión con Supabase
DB_HOST = os.getenv("DB_HOST")  # URL de la base de datos
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")  # Puerto por defecto de PostgreSQL

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    st.success("Conexión exitosa a la base de datos de Supabase")
except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")
    st.stop()

# Función para cargar datos de la tabla Articulo
def cargar_datos():
    query = """
    SELECT 
        Articulo.titulo_articulo, 
        Articulo.fecha_publicacion, 
        Articulo.anio_publicacion, 
        Articulo.doi,
        Estudiante.Nombres || ' ' || Estudiante.Apellidos AS autor,
        Institucion.nombre_institucion,
        Indizacion.nombre_revista,
        Indizacion.base_datos,
        Indizacion.quartil
    FROM Articulo
    JOIN Estudiante ON Articulo.estudiante_id = Estudiante.id
    JOIN Institucion ON Articulo.institucion_id = Institucion.id
    JOIN Indizacion ON Articulo.indizacion_id = Indizacion.id;
    """
    df = pd.read_sql_query(query, conn)
    return df

# Mostrar los datos en Streamlit
st.title("Visualización de Artículos Publicados")
dataframe = cargar_datos()
st.dataframe(dataframe)

# Cerrar la conexión
conn.close()
