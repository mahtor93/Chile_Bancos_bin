import asyncio
import aiohttp
import json
import os
from bs4 import BeautifulSoup
from unidecode import unidecode
from clear_data import clear_data
from format_data import format_data
from sort import sort_data

async def fetch_data(session, url):
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Solicitud fallida para {url}. Estado: {response.status}")
                return None
    except asyncio.TimeoutError:
        print(f"Tiempo de espera agotado para {url}")
        return None


async def main():
    async with aiohttp.ClientSession() as session:
        web_response = await fetch_data(session, 'https://bincheck.io/es/bin-list')
        if web_response:
            print('Conexión exitosa')
            major_soup = BeautifulSoup(web_response,'html.parser')
            country_url = major_soup.find_all('a',attrs={'class':'flex items-start inline-block gap-3 p-5 space-x-4 transition ease-in-out border rounded-md border-slate-200 duraton-150 hover:border hover:border-blue-400 dark:border-slate-500 dark:hover:border-blue-400 country'})
            for url in country_url:
                cls_url = url.get('href')
                print(cls_url)
                response = await fetch_data(session, "https://bincheck.io/es"+cls_url)
                if response:
                    print('Conexión exitosa')
                    soup = BeautifulSoup(response, 'html.parser')
                    name_country = soup.find('h2',attrs={'class':'inline-block px-2 mb-4 text-base font-semibold leading-normal tracking-wide text-gray-800 bg-yellow-200 sm:text-lg'})
                    name_country = name_country.text.strip().replace(" ","_").lower()
                    links = soup.find_all('a', attrs={'class': 'flex items-start inline-block gap-3 p-5 space-x-4 transition ease-in-out border rounded-md border-slate-200 duraton-150 hover:border hover:border-blue-400 dark:border-slate-500 dark:hover:border-blue-400 bank'})
                    tasks = []
                    data = []
                    for link in links:
                        href = link.get('href')
                        tasks.append(fetch_data(session, href))
                    responses = await asyncio.gather(*tasks)
                    for res in responses:
                        if res:
                            soup_link = BeautifulSoup(res, 'html.parser')
                            name = soup_link.find('h2', attrs={'class': 'inline-block px-2 mb-4 text-base font-semibold leading-normal tracking-wide text-gray-800 bg-yellow-200 sm:text-lg'})
                            name = name.text.replace(" - CHILE", "").replace(" S.A. ", "").replace(",", "").replace("s.a.", "").replace("S.A.", "").rstrip().replace(" ", "_").replace("/", " ")
                            table_link = soup_link.find('table')
                            headers = [unidecode(th.text.strip().replace("\n", "")) for th in table_link.find('thead').find_all('th')]
                            table_data = []
                            for fila in table_link.find('tbody').find_all('tr'):
                                row_data = {}
                                for index, celda in enumerate(fila.find_all('td')):
                                    dato = unidecode(celda.text.strip().replace("\n", "").replace("\u2197", ""))
                                    row_data[headers[index]] = dato.rstrip()
                                table_data.append(row_data)
                            data.append({name: table_data})  # Agregamos los datos al diccionario
                    # Guardar todos los datos en un solo archivo JSON
                    if not os.path.exists(name_country):
                        os.makedirs(name_country)

                    with open(name_country+"/datos_bancarios_name.json", 'w') as archivo:
                        json.dump(data, archivo, indent=4)
                    
                    clear_data(name_country+"/datos_bancarios_name.json", name_country+"/datos_bancarios_sort.json")
                    format_data(name_country+"/datos_bancarios_sort.json",name_country+"/datos_bancarios_sort.json")
                    sort_data(name_country+"/datos_bancarios_sort.json",name_country+"/datos_bancarios_sort.json")

if __name__ == "__main__":
    asyncio.run(main())