import json

def format_data(input_file, output_file):
    def transformar_formato(diccionario_original):
        nuevo_diccionario = {
            "bin": diccionario_original["Numero BIN/IIN"],
            "country": diccionario_original["Pais"],
            "bank": diccionario_original["Nombre del emisor / Banco"],
            "network": diccionario_original["Marca de carro"],
            "type": diccionario_original["Tipo de tarjeta"],
            "level": diccionario_original["Nivel de tarjeta"]
        }
        return nuevo_diccionario

    # Leer el JSON desde el archivo
    with open(input_file, 'r') as file: #'datos_bancarios_limpios.json'
        datos_originales = json.load(file)

    # Transformar cada objeto en el formato deseado
    datos_transformados = [transformar_formato(objeto) for objeto in datos_originales]

    # Guardar los datos transformados en el mismo archivo
    with open(output_file, 'w') as file: #'datos_bancarios_limpios.json'
        json.dump(datos_transformados, file, indent=4)

    print('Datos formateados y guardados exitosamente en el mismo archivo.')
