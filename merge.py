import json
import os

# Directorio donde se encuentran los archivos JSON
directorio = './USA/'
# Nombre del archivo de salida que contendrá todos los datos
archivo_salida = 'datos_completos.json'

datos_completos = []

# Leer todos los archivos JSON en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('.json'):
        with open(os.path.join(directorio, archivo), 'r') as f:
            datos_archivo = json.load(f)
            datos_completos.extend(datos_archivo)

# Escribir los datos combinados en un solo archivo JSON
with open(archivo_salida, 'w') as f:
    json.dump(datos_completos, f, indent=4)

print(f'Datos combinados guardados en {archivo_salida}')
