from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


# Configurar Selenium
##chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
##service = Service("C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe")  # Ruta al controlador de ChromeDriver
driver = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe")

#Obtiene los datos historicos del jugador ingresado
def get_player_data_history(url_player):
    url_player = url_player.replace('Show','History')
    driver.get(url_player)

    # Encontrar la tabla
    table = driver.find_element(By.ID, "player-tournament-stats")
    rows = table.find_elements(By.TAG_NAME, "tr")

    seasons = []
    teams = []
    matchs = []
    matchs_played = []
    minutes = []
    goals = []
    assists = []
    ratings = []

    # Extraer los datos de la tabla
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 16:
            season = cells[0].text
            team = cells[1].text
            match = cells[4].text
            match_played = cells[5].text
            minute = cells[6].text
            goal = cells[7].text
            assist = cells[8].text
            rating = cells[15].text


        seasons.append(season)
        teams.append(team)
        matchs.append(match)
        matchs_played.append(match_played)
        minutes.append(minute)
        goals.append(goal)
        assists.append(assist)
        ratings.append(rating)

    data = {
    'Temporada' : seasons,
    'equipo' : teams,
    'Campeonato': matchs,
    'Partidos Jugados': matchs_played,
    'Minutos': minutes,
    'Goles': goals,
    'Asistencias': assists,
    'Rating': ratings}

    # Crear un DataFrame con los datos recolectados

    df = pd.DataFrame(data)
    print(df)

    df.to_csv('datos-estadicticos.csv',sep=';',index=False)

        

#Obtiene los jugadores y sus links, posteriormente los almacena en listas
def player_and_link(entry):
    # Navegar a la página web
    url = 'https://es.whoscored.com/Search/?t='+entry
    driver.get(url)

    # Esperar a que la página se cargue 
    driver.implicitly_wait(10)

    try:
    # Encontrar todos los elementos de enlace que contienen los jugadores
        table = driver.find_element(By.CLASS_NAME, "search-result")
        rows = table.find_elements(By.TAG_NAME, "tr")

        players = []
        links = []

        for row in rows[1:]:
            # Busca el primer elemento que encuentre con el css_selector
            cell = row.find_element(By.TAG_NAME, 'a')
            name_player = cell.text

            # LLama a la variable que contiene el primer parametro y obtiene el atributo de href
            url_player = cell.get_attribute('href')

            players.append(name_player.upper())
            links.append(url_player)

        data = {'Players':players,
                'Links':links}
        
    except NoSuchElementException:
        print('This player no exist \n')
        data = False

    return data


#Vaida la eleccion de jugador si se encuentran varios 
def get_player_url(player_name):
    #Llama a la funcion player_and_link(entry) y almacena en una variable
    player_entered = player_and_link(player_name)

    #Retorna falso si no se encuentra el jugador 
    if player_entered == False:
        url_got = False
    
    else:
        #Convertimos los datos de la variable player_entered en un DataFrame
        df = pd.DataFrame(player_entered)
        #Imprime los jugadores encontrados como opciones para seleccionar
        print(df.to_string())
        #Comprueba si existen mas de 2 jugadores con el mismo nombre
        
        
        if len(player_entered['Players']) >= 2:
            print("Existe varios jugadores con este nombre, escriba y sea mas especifico o digite uno de los números: ")
            opcion = input('Escriba nombre / Digite: ')

            if opcion.isnumeric():
                opcion = int(opcion)
                player_got = player_entered['Players'][opcion]
                url_got = player_entered['Links'][opcion]

            else:
                opcion = opcion.upper()
                for name in player_entered['Players']:
                    if opcion in name:
                        index = player_entered['Players'].index(name)
                        player_got = player_entered['Players'][index]
                        url_got = player_entered['Links'][index]

    return url_got


name_player = input('Ingrese nombre de jugador: ').upper()
url_player = get_player_url(name_player)
print(url_player)
history_player = get_player_data_history(url_player)
print(history_player)




