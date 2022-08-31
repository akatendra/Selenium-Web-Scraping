from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import scraper
import time
from datetime import timedelta, datetime
from bs4 import BeautifulSoup


def spent_time():
    global start_time
    sec_all = time.time() - start_time
    if sec_all > 60:
        minutes = sec_all // 60
        sec = sec_all % 60
        time_str = f'| {int(minutes)} min {round(sec, 1)} sec'
    else:
        time_str = f'| {round(sec_all, 1)} sec'
    start_time = time.time()
    return time_str


def run_process(page_number, browser):
    if scraper.connect_to_base(browser, page_number):
        time.sleep(2)
        html = browser.page_source
        output_data = scraper.parse_html_kvartiry_vtorichka(html)
        scraper.write_to_database(output_data)
    else:
        print("Error connecting to page")


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


start_time = time.time()
print('Beginning...')
options = webdriver.FirefoxOptions()
#  Will launch browser without UI(headless)
# options.add_argument('headless')


print('FireFox options added...', spent_time())

FIREFOX_PATH = 'd:\\Python\\geckodriver-v0-31-0-win64\\geckodriver.exe'
service = Service(FIREFOX_PATH)
browser = webdriver.Firefox(service=service, options=options)
URL = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/vtorichka'
# URL = 'f:\\INTERNET_files\\avito.html'
BASE = 'https://www.avito.ru'
print('Opening browser...', spent_time())

browser.get(URL)
# Sleep for 2 seconds
time.sleep(2)
# Scroll down page
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print('browser opened', spent_time())
page_source = browser.page_source
print('page_source_spent_time:', spent_time())
print('Current URL:', browser.current_url)
soup = BeautifulSoup(page_source, 'lxml')
items = soup.select('div[data-marker="item"]')
print('######################################################################')
print('items:', len(items))
print('######################################################################')
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
        item_type = item_number_of_rooms_list[0]
    print('item_number_of_rooms:', item_number_of_rooms)
    print('item_type:', item_type)
    if len(item_title_list) > 3:
        item_area = float(
            (item_title_list[1] + '.' + item_title_list[2]).replace('\xa0м²',
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
    item_date_str = str(item_date)
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
    print('###############################################################')
print('items:', len(data), data)

