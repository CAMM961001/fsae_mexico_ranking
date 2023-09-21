# ---------------------------------------------------------- CARGA DE LIBRERÍAS
import os
import re
import requests

from bs4 import BeautifulSoup
from pandas import DataFrame


# ----------------------------------------------------  DEFINICIÓN DE VARIBALES
ROOT = os.getcwd()

# Contenido de página de resultados
URLS_RESULTADOS_ANUALES = 'https://www.sae.org/attend/student-events/formula-sae-michigan/awards-results'
PAGINA = requests.get(url=URLS_RESULTADOS_ANUALES)
CONTENIDO = BeautifulSoup(markup=PAGINA.text, features='html.parser')


# ----------------------------------------------------- DEFINICIÓN DE FUNCIONES
def extraer_url_de_cadena_html(cadena):
    # Extraer url de cadena tipo <a href="url"></a>
    coincide = re.search(r'href="([^"]+)"', cadena)
    if coincide:
        return coincide.group(1)
    return None


# ----------------------------------------------------------- TRABAJO PRINCIPAL
# Extraer tabla de resultados
tabla_objetivo = CONTENIDO.find_all(name='table')[0]

# Extraer filas de la tabla
tabla_objetivo_filas = tabla_objetivo.find_all(name='tr')

# Extraer nombres de columnas
columnas = tabla_objetivo_filas.pop(0).text.strip().split('\n\n\n')
columnas = [col.replace('\xa0', '') for col in columnas]

# Iniciar diccionario de datos extraidos
datos_extraidos = dict()

for fila in tabla_objetivo_filas:
    # Lista de elementos contenidos en fila
    fila = fila.find_all(name='td')
    
    # Extraer datos de cada elemento de la lista
    valores_en_fila = [val.find_all(name='p') for val in fila]
    
    # Lista para almacenar datos limpios
    temp = list()
    for idx, val in enumerate(valores_en_fila):
        # Tratamiento especial para datos de año (Primera columna)
        if idx == 0:
            temp.append(val[0].get_text())
            continue
        
        # Generar lista de urls dentro de cada elemento de la fila
        urls = [str(cursor.find(name='a', href=True)) for cursor in val]
        urls = [extraer_url_de_cadena_html(cadena) for cadena in urls]

        # Extraer elemento único en lista de urls en caso de None
        if len(urls) == 1 and urls[0] == None:
            urls = urls[0]

        # Completar dirección de internet en caso de incompleto
        else:
            urls = [
                'https://www.sae.org' + url 
                if not url.startswith('http') else url
                for url in urls]

        temp.append(urls)

    # Construir diccionario de información
    datos_extraidos[int(temp[0])] = temp[1:]

# Construir dataframe de datos extraidos
datos = DataFrame.from_dict(
    data=datos_extraidos
    ,orient='index'
    ,columns=columnas)

# Reemplazar salidas de lista vacía por nan
datos = datos.mask(datos.map(func=str).eq(other='[]'))

# Almacenar datos a archivo externo
datos.to_csv(os.path.join(ROOT, 'datos', 'urls_resultados_anuales.csv'))

if __name__ == '__main__':
    print('Trabajo ejecutado...')
