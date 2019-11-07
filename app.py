import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&brand=mitsubishi&city_distance=0&without_price=1'
total_cars = 0
cars = {}

while True:
    response = requests.get(url)
    data = response.content

    soup = BeautifulSoup(data, 'lxml')

    containter = soup.find_all('article', {'class': 'single-classified'})

    for car in containter:
        title_tag = car.find('img')['alt']
        title = title_tag if title_tag else 'N/A'
        price_tag = car.get('data-price')
        price = price_tag if price_tag else 'N/A'
        try:
            year = car.find_all('div', {'class': 'inline-block'})[0].text
        except:
            year = 'N/A'
        try:
            km = car.find_all('div', {'class': 'inline-block'})[1].text
        except:
            km = 'N/A'
        try:
            fuel_type = car.find_all('div', {'class': 'inline-block'})[2].text
        except:
            fuel_type = 'N/A'
        try:
            eng_volume = car.find_all('div', {'class': 'inline-block'})[3].text
        except:
            eng_volume = 'N/A'
        try:
            body_type = car.find_all('div', {'class': 'inline-block'})[4].text
        except:
            body_type = 'N/A'
        try:
            power = car.find_all('div', {'class': 'inline-block'})[5].text
        except:
            power = 'N/A'
        try:
            gear_box = car.find_all('div', {'class': 'inline-block'})[6].text
        except:
            gear_box = 'N/A'


        total_cars += 1
        cars[total_cars] = [title, price, year, km, fuel_type, eng_volume, body_type, power, gear_box]

    url_tag = soup.find('a', {'title': 'Sledeća stranica'})
    if url_tag:
        url = 'https://www.polovniautomobili.com' + url_tag.get('href')
    else:
        break
cars_df = pd.DataFrame.from_dict(cars, orient='index', columns=['Title', 'Price', 'Year', 'Distance passed', 'Fuel Type',
                                                                'Engine Volume', 'Type', 'Power', 'Gear Box'])
cars_df.to_csv('mitsubishi.csv')

print(total_cars)
