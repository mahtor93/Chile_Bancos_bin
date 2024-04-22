import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from unidecode import unidecode

async def fetch_data(session, url):
    try:
        async with session.get(url, timeout=10) as response:
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
        response = await fetch_data(session, "AQUI_VA_LA_URL_PARA_FARMEAR")
        if response:
            print('Conexión exitosa')
            soup = BeautifulSoup(response, 'html.parser')
            links = soup.find_all('a', attrs={'class': 'flex items-start inline-block gap-3 p-5 space-x-4 transition ease-in-out border rounded-md border-slate-200 duraton-150 hover:border hover:border-blue-400 dark:border-slate-500 dark:hover:border-blue-400 bank'})
            #reads = 0
            #response_index = 0  # Variable para contar las respuestas
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
            with open("datos_bancarios.json", 'w') as archivo:
                json.dump(data, archivo, indent=4)

if __name__ == "__main__":
    asyncio.run(main())