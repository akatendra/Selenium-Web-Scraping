import requests
import time
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_chrome_browser():
    options = webdriver.ChromeOptions()
    # Unable to hide "Chrome is being controlled by automated software" infobar
    options.add_experimental_option("excludeSwitches",
                                    ['enable-automation'])
    # Open Chrome for full size of screen
    options.add_argument("--start-maximized")
    # chrome_options.add_argument('--incognito')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--disable-extensions') #  ?
    #  Will launch browser without UI(headless)
    options.add_argument("--headless")
    # инициализируем драйвер с нужными опциями
    CHROME_PATH = 'd:\\Python\\chromedriver_win32\\chromedriver.exe'
    service = Service(CHROME_PATH)
    browser = webdriver.Chrome(service=service, options=options)
    return browser


def get_firefox_browser():
    options = webdriver.FirefoxOptions()
    #  Will launch browser without UI(headless)
    # options.add_argument('headless')
    FIREFOX_PATH = 'd:\\Python\\geckodriver-v0-31-0-win64\\geckodriver.exe'
    service = Service(FIREFOX_PATH)
    browser = webdriver.Firefox(service=service, options=options)
    return browser


def connect_to_page(browser, URL, page_number=1):
    if page_number == 1:
        page_url = URL
    else:
        page_url = f'{URL}?p={page_number}'
    browser.get(page_url)



def convert_date(date):
    if 'мин' in date:
        date_list = date.split()
        minutes = int(date_list[0])
        converted_date = datetime.now() - timedelta(minutes=minutes)
    elif 'час' in date:
        date_list = date.split()
        hours = int(date_list[0])
        converted_date = datetime.now() - timedelta(hours=hours)
    elif 'день' or 'дня' or 'дней' in date:
        date_list = date.split()
        days = int(date_list[0])
        converted_date = datetime.now() - timedelta(days=days)
    elif 'недел' in date:
        date_list = date.split()
        weeks = int(date_list[0])
        converted_date = datetime.now() - timedelta(weeks=weeks)
    else:
        converted_date = datetime.now()
    converted_date.strftime("%Y-%m-%d %H:%M")
    return converted_date


def parse_html(html):
    BASE = 'https://www.avito.ru'
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div[data-marker="item"]')
    print('##################################################################')
    print('items:', len(items))
    print('##################################################################')
    data = {}
    for item in items:
        data_item_id = int(item['data-item-id'])
        print('data_item_id:', data_item_id)
        item_id = item['id']
        print('item_id:', item_id)
        item_a = item.select_one('a[data-marker="item-title"]')
        print('item_a:', item_a)
        item_url = BASE + item_a['href']
        print('item_url:', item_url)
        item_title = item_a.find('h3').text
        print('item_title:', item_title)
        item_title_list = item_title.split(',')
        print('item_title_list:', item_title_list)
        item_number_of_rooms_list = None
        item_number_of_rooms = None
        item_type = None
        if '-к.' in item_title_list[0]:
            item_number_of_rooms_list = item_title_list[0].split()
            print('item_number_of_rooms_list:', item_number_of_rooms_list)
            item_number_of_rooms_list_len = len(item_number_of_rooms_list)
            if item_number_of_rooms_list_len == 1:
                item_number_of_rooms = None
                item_type = item_number_of_rooms_list[0]
            elif item_number_of_rooms_list_len == 2:
                item_number_of_rooms = int(
                    item_number_of_rooms_list[0].replace('-к.', ''))
                item_type = item_number_of_rooms_list[1]
            elif item_number_of_rooms_list_len == 3:
                item_number_of_rooms = int(
                    item_number_of_rooms_list[1].replace('-к.', ''))
                item_type = item_number_of_rooms_list[2]
        else:
            item_number_of_rooms = None
            item_type = item_title_list[0]
        print('item_number_of_rooms:', item_number_of_rooms)
        print('item_type:', item_type)
        if len(item_title_list) > 3:
            item_area = float(
                (item_title_list[1] + '.' + item_title_list[2]).replace(
                    '\xa0м²',
                    ''))
        else:
            item_area = int(item_title_list[1].replace('\xa0м²', ''))
        print('item_area:', item_area)
        item_floor_house = item_title_list[-1].replace('\xa0эт.', '')
        print('item_floor_house:', item_floor_house)
        item_floor_house_list = item_floor_house.split('/')
        print('item_floor_house_list:', item_floor_house_list)
        item_floor = int(item_floor_house_list[0].replace(' ', ''))
        print('item_floor:', item_floor)
        item_floors_in_house = int(item_floor_house_list[1].replace(' ', ''))
        print('item_floors_in_house:', item_floors_in_house)
        item_price_str = item.select_one('span[class*="price-text-"]').text
        print('item_price_str:', item_price_str)
        item_price = int(
            ''.join(char for char in item_price_str if char.isdecimal()))
        print('item_price:', item_price)
        item_currency = item.select_one('span[class*="price-currency-"]').text
        print('item_currency:', item_currency)
        item_address = item.select_one('span[class*="geo-address-"]').find(
            'span').text
        print('item_address:', item_address)
        item_city = item.select_one('div[class*="geo-georeferences-"]').find(
            'span').find('span').text
        # item_city = item_city0.find('span').text
        print('item_city:', item_city)
        item_date_data = item.select_one('div[data-marker="item-date"]').text
        item_date = convert_date(item_date_data)
        # Remove the fractional part of the seconds after the dot
        item_date_list = str(item_date).split('.')
        item_date_str = item_date_list[0]
        item_date_timestamp = datetime.timestamp(item_date)
        print('item_date:', item_date)
        item_dict = {'data_item_id': data_item_id,
                     'item_id': item_id,
                     'item_url': item_url,
                     'item_title': item_title,
                     'item_type': item_type,
                     'item_number_of_rooms': item_number_of_rooms,
                     'item_area': item_area,
                     'item_floor_house': item_floor_house,
                     'item_floor': item_floor,
                     'item_floors_in_house': item_floors_in_house,
                     'item_price': item_price,
                     'item_currency': item_currency,
                     'item_address': item_address,
                     'item_city': item_city,
                     'item_date': item_date,
                     'item_date_timestamp': item_date_timestamp,
                     'item_date_str': item_date_str
                     }
        data[item_id] = item_dict
        print('##############################################################')
    print('items:', len(data), data)
    return data


def get_load_time(item_url):
    try:
        # устанавливаем значения заголовков запроса
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        # делаем запрос по url статьи article_url
        response = requests.get(
            item_url, headers=headers, stream=True, timeout=3.000
        )
        # получаем время загрузки страницы
        load_time = response.elapsed.total_seconds()
    except Exception as e:
        print(e)
        load_time = "Loading Error"
    return load_time
