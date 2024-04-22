import json

# Cargar los datos del archivo JSON
with open("datos_bancarios.json", 'r') as archivo:
    data = json.load(archivo)

# Crear una lista vacía para almacenar todos los datos
all_data = []

# Iterar sobre cada diccionario en la lista
for banco_info in data:
    # Obtener los valores asociados al nombre del banco
    info = list(banco_info.values())[0]
    # Extender la lista general con los datos de este banco
    all_data.extend(info)

# Guardar los datos en el mismo archivo JSON
with open("datos_bancarios_limpios.json", 'w') as archivo:
    json.dump(all_data, archivo, indent=4)
