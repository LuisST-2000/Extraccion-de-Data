from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random


#("C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe")  # Ruta al controlador de ChromeDriver
driver = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe")


def get_all_matchs_livesport():
    url = "https://www.livesport.com/es/futbol/"
    driver.get(url)
    
    wait = WebDriverWait(driver, 30)
    wait

    # Encontrar todos los elementos de partidos de hoy
    matchs = driver.find_elements(By.CLASS_NAME, "event__match")

    # Obtener los detalles de cada partido
    for match in matchs:

        try:
            match_state = match.find_element(By.CLASS_NAME, "event__stage--block").text
            score_home = match.find_element(By.CLASS_NAME, "event__score--home").text
            score_away = match.find_element(By.CLASS_NAME, "event__score--away").text
            score = score_home + ' - ' + score_away
        except NoSuchElementException:
            match_state = match.find_element(By.CLASS_NAME, "event__time").text
            score = 'Preview'

        team_home = match.find_element(By.CLASS_NAME, "event__participant--home").text
        team_away = match.find_element(By.CLASS_NAME, "event__participant--away").text

        print("Estado: ", match_state)
        print("Equipo local:", team_home)
        print("Equipo visitante:", team_away)
        print("Score: ", score)
        print()  # Agregar una línea en blanco para separar los partidos

def get_data_footablldatabse():

    url = "https://www.footballdatabase.eu/es/jugador/detalles/7545-paolo-guerrero"
    driver.get(url)

    WebDriverWait(driver, 60)


    driver.execute_script("""
            for (let i of document.getElementsByClassName('inside')){
                i.style.opacity = 0;
            }
        """)

    table = driver.find_element(By.TAG_NAME, 'main')
    result_search = table.find_elements(By.CLASS_NAME, 'row')

    clubs = []
    partidos_jugados = []
    goles = []
    efectividad = []
    minutos_jugados = []
    once_inicial = []
    victorias = []
    derrotas = []
    for tr in result_search[3:4]:
        cells = tr.find_element(By.CLASS_NAME, 'firstblock')
        asd = cells.find_elements(By.TAG_NAME, 'tr')
        for i in asd[1:]:
            line = i.find_elements(By.TAG_NAME, 'td')
            time.sleep(random.randint(4,8))
            club = line[0].text
            partidos = line[1].text
            gol = line[2].text
            efect = line[4].text
            minutos = line[5].text
            inicial = line[8].text
            victoria = line[9].text
            derrota = line[10].text

            clubs.append(club)
            partidos_jugados.append(partidos)
            goles.append(gol)
            efectividad.append(efect)
            minutos_jugados.append(minutos)
            once_inicial.append(inicial)
            victorias.append(victoria)
            derrotas.append(derrota)

    data = {'Clubs': clubs,
                'Partidos Jugados' : partidos_jugados,
                'Goles': goles,
                'Efectividad' : efectividad,
                'Minutos Jugados': minutos_jugados,
                'Once Inicial': once_inicial,
                'Victorias':victorias,
                'Derrotas': derrotas}
        

    df = pd.DataFrame(data)
    print(df)
    
driver.quit()





'''
fecha_ingresada = input("Ingrese ps: ")

# Esperar a que la página se cargue completamente (ajusta el tiempo según sea necesario)
wait = WebDriverWait(driver, 30)
wait
# Encontrar todos los elementos de partidos de hoy
calendar = driver.find_elements(By.CLASS_NAME, "calendar")
for date in calendar:
    click_calendar = date.find_element(By.ID,"calendarMenu")
    click_calendar.click()
    date_cells = date.find_elements(By.CLASS_NAME,'calendar__listItem')
    fecha_elements = [element.find_element(By.TAG_NAME, 'button') for element in date_cells]
    for fecha_element in fecha_elements:
        fecha = fecha_element.text
        if fecha_ingresada in fecha:
            fecha_element.click()
            wait
driver.quit()'''



