import json

# Cargar el JSON desde el archivo
with open('./USA/datos_bancarios_limpios.json', 'r') as file:
    jsonData = json.load(file)

# Ordenar el JSON según el número BIN
jsonData.sort(key=lambda x: x['bin'])  # Suponiendo que el número BIN está almacenado en el campo "bin"

# Guardar el JSON ordenado en un nuevo archivo
with open('./USA/datos_bancarios_sort.json', 'w') as file:
    json.dump(jsonData, file, indent=2)

print('JSON ordenado y guardado exitosamente.')
