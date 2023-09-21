# ---------------------------------------------------------- CARGA DE LIBRERÍAS
import os
import ast
import requests
import pandas as pd


# ----------------------------------------------------  DEFINICIÓN DE VARIBALES
ROOT = os.getcwd()
DIR_SALIDA = os.path.join(ROOT, 'datos', 'resultados')
os.makedirs(DIR_SALIDA, exist_ok=True)

# Archivo de urls para consulta
URLS_PATH = os.path.join(ROOT, 'datos', 'urls_resultados_anuales.csv')
URLS = pd.read_csv(URLS_PATH, index_col=0)


# ----------------------------------------------------------- TRABAJO PRINCIPAL
k = 0
for anio in URLS.index:
    print(f"Descargando archivos {anio}...")

    # Crear directorio de almacenamiento
    directorio = os.path.join(DIR_SALIDA, str(anio))
    os.makedirs(directorio, exist_ok=True)

    # Filtrar competencias con información
    datos = URLS.loc[anio][~URLS.loc[anio].isna()]
    competencias = list(datos.index)

    # Para cada competencia se consultan y almacenan los documentos
    for competencia in competencias:
        docs = ast.literal_eval(datos[competencia])

        # Descargar y almacenar cada documento de cada competencia
        for doc in docs:
            # Nombre de archivo
            nombre_archivo = doc.split('/')[-1].replace('?name=', '')

            # Descargar archivo de internet
            archivo_internet = requests.get(doc)

            # Almacenar archivo en directorio correspondiente
            nombre_archivo = os.path.join(directorio, nombre_archivo)
            with open(file=nombre_archivo, mode='wb') as archivo:
                archivo.write(archivo_internet.content)

            # Contador de archivos descargados
            k += 1

print(f"Total de archivos descargados: {k}")


if __name__ == '__main__':
    print('Trabajo ejecutado...')
