import requests
import json
from bs4 import BeautifulSoup
from unidecode import unidecode

# Formateo de la página para mejorar lectura
def get_soup(response_value):
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

# Obtención de todos los enláces de interés
def get_entidades_link(soup_source):
    links = soup_source.find_all('a', attrs={'class':'flex items-start inline-block gap-3 p-5 space-x-4 transition ease-in-out border rounded-md border-slate-200 duraton-150 hover:border hover:border-blue-400 dark:border-slate-500 dark:hover:border-blue-400 bank'})
    return links

def look_in_links(arr_links):
    for link in arr_links:
        href = link.get('href')
        res = requests.get(href)
        if(res.status_code == 200):
            print(href+" is OK")
        else:
            print(href + " is Down")

## Response obtiene toda la página donde están listadas las entidades bancarias
response = requests.get("")
if response.status_code == 200:
    print('conectado')
    soup = get_soup(response)
    links = get_entidades_link(soup)
    for link in links:
        res = requests.get(link.get('href'))
        if(res.status_code==200):
            print('Link accesado: '+link.get('href'))
            soup_link = BeautifulSoup(res.text, 'html.parser')
            name = soup_link.find('h2', attrs={'class':'inline-block px-2 mb-4 text-base font-semibold leading-normal tracking-wide text-gray-800 bg-yellow-200 sm:text-lg'})
            name = name.text.replace(" - CHILE","").replace(" S.A. ","").replace(",","").replace("s.a.","").replace("S.A.","").rstrip().replace(" ","_")
            print(name)
            table_link = soup_link.find('table')
            headers = [unidecode(th.text.strip().replace("\n","")) for th in table_link.find('thead').find_all('th')]
            table_data = []
            for fila in table_link.find('tbody').find_all('tr'):
                row_data = {}  # Inicializar el diccionario dentro del bucle
                for index, celda in enumerate(fila.find_all('td')):
                    dato = unidecode(celda.text.strip().replace("\n","").replace("\u2197",""))
                    row_data[headers[index]] = dato.rstrip()
                table_data.append(row_data)
            json_table = json.dumps(table_data, indent=4)
            print(json_table)
            with open(name+'.json','w') as archivo:
                archivo.write(json_table)

    