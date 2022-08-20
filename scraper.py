import requests
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import logging
import logging.config

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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
    browser = webdriver.Firefox(service=service, options=options, service_log_path=None)
    return browser


def connect_to_page(browser, URL, page_number=1):
    if page_number == 1:
        page_url = URL
    else:
        page_url = f'{URL}?p={page_number}'
    browser.get(page_url)


def convert_date(date):
    if 'сек' in date:
        date_list = date.split()
        sec_str = date_list[0]
        if sec_str.isdigit():
            sec = int(date_list[0])
            converted_date = datetime.now() - timedelta(seconds=sec)
        else:
            converted_date = datetime.now()
    elif 'мин' in date:
        date_list = date.split()
        minutes_str = date_list[0]
        if minutes_str.isdigit():
            minutes = int(date_list[0])
            converted_date = datetime.now() - timedelta(minutes=minutes)
        else:
            converted_date = datetime.now()
    elif 'час' in date:
        date_list = date.split()
        hours_str = date_list[0]
        if hours_str.isdigit():
            hours = int(date_list[0])
            converted_date = datetime.now() - timedelta(hours=hours)
        else:
            converted_date = datetime.now()
    elif 'день' or 'дня' or 'дней' in date:
        date_list = date.split()
        days_str = date_list[0]
        if days_str.isdigit():
            days = int(days_str)
            converted_date = datetime.now() - timedelta(days=days)
        else:
            converted_date = datetime.now()
    elif 'недел' in date:
        date_list = date.split()
        weeks_str = date_list[0]
        if weeks_str.isdigit():
            weeks = int(date_list[0])
            converted_date = datetime.now() - timedelta(weeks=weeks)
        else:
            converted_date = datetime.now()
    elif 'мес' in date:
        date_list = date.split()
        month_str = date_list[0]
        if month_str.isdigit():
            month = int(date_list[0])
            converted_date = datetime.now() - timedelta(days=30 * month)
        else:
            converted_date = datetime.now()
    else:
        converted_date = datetime.now()
    converted_date.strftime("%Y-%m-%d %H:%M")
    return converted_date


def parse_html(html):
    BASE = 'https://www.avito.ru'
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div[data-marker="item"]')
    logger.warning(
        '##################################################################')
    logger.warning(f'items:  {len(items)}')
    logger.warning(
        '##################################################################')
    data = {}
    for item in items:
        # We intercept the error in case some fields are not filled while
        # parsing. An error during parsing causes the whole process to stop.
        # In case of an error, we move on to parsing the next item.
        try:
            data_item_id = int(item['data-item-id'])
            logger.warning(f'data_item_id:  {data_item_id}')
            item_id = item['id']
            logger.warning(f'item_id:  {item_id}')
            item_a = item.select_one('a[data-marker="item-title"]')
            logger.warning(f'item_a:  {item_a}')
            item_url = BASE + item_a['href']
            logger.warning(f'item_url:  {item_url}')
            item_title = item_a.find('h3').text
            # Intercepting and processing errors in the title
            # of the announcement. Check is the title exist or not. There was
            # a case where the title field was not filled in for some reason,
            # and it caused a parsing error.
            if item_title:
                logger.warning(f'item_title:  {item_title}')
                item_title_list = item_title.split(',')
                logger.warning(f'item_title_list:  {item_title_list}')
                # item_number_of_rooms_list = None
                item_number_of_rooms = None
                item_type = None
                if '-к.' in item_title_list[0]:
                    item_number_of_rooms_list = item_title_list[0].split()
                    logger.warning(f'item_number_of_rooms_list: {item_number_of_rooms_list}')
                    item_number_of_rooms_list_len = len(
                        item_number_of_rooms_list)
                    # If the number of rooms is not specified (Апартаменты,
                    # Апартаменты-студия, Квартира-студия, Апартаменты-студия,
                    # Своб. планировка
                    if item_number_of_rooms_list_len == 1:
                        item_number_of_rooms = None
                        item_type = item_number_of_rooms_list[0].lower()
                    # Стандартный вариант в большинстве случаев
                    elif item_number_of_rooms_list_len == 2:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[0].replace('-к.', ''))
                        item_type = item_number_of_rooms_list[1]
                    # There was a variant when the number of rooms was preceded
                    # by the word: Аукцион:
                    elif item_number_of_rooms_list_len == 3:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[1].replace('-к.', ''))
                        item_type = item_number_of_rooms_list[2]
                else:
                    item_number_of_rooms = None
                    item_type = item_title_list[0].lower()
                logger.warning(f'item_number_of_rooms:  {item_number_of_rooms}')
                logger.warning(f'item_type:  {item_type}')

                # Getting an apartment area
                if len(item_title_list) > 3:
                    item_area = float(
                        (item_title_list[1] + '.' + item_title_list[
                            2]).replace(
                            '\xa0м²',
                            ''))
                else:
                    item_area = int(item_title_list[1].replace('\xa0м\xb2', ''))
                logger.warning(f'item_area:  {item_area}')

                # Getting the floor on which the apartment is located and the
                # number of floors of the building
                item_floor_house = item_title_list[-1].replace('\xa0эт.',
                                                               '').strip()
                logger.warning(f'item_floor_house:  {item_floor_house}')
                item_floor_house_list = item_floor_house.split('/')
                logger.warning(f'item_floor_house_list: {item_floor_house_list}')
                item_floor = int(item_floor_house_list[0].replace(' ', ''))
                logger.warning(f'item_floor:  {item_floor}')
                item_floors_in_house = int(
                    item_floor_house_list[1].replace(' ', ''))
                logger.warning(f'item_floors_in_house:  {item_floors_in_house}')
            else:
                item_title = None
                item_type = None
                item_number_of_rooms = None
                item_area = None
                item_floor_house = None
                item_floor = None
                item_floors_in_house = None

            # Getting an item price.
            item_price_str = item.select_one('span[class*="price-text-"]').text
            logger.warning(f'item_price_str:  {item_price_str}')
            item_price = int(
                ''.join(char for char in item_price_str if char.isdecimal()))
            logger.warning(f'item_price:  {item_price}')

            # Getting an item price currency.
            item_currency = item.select_one(
                'span[class*="price-currency-"]').text
            logger.warning(f'item_currency:  {item_currency}')

            # Getting an item address.
            item_geo_address = item.select_one('span[class*="geo-address-"]')
            if item_geo_address:
                item_address = item_geo_address.find('span').text
            else:
                item_address = None
            logger.warning(f'item_address:  {item_address}')

            # Getting an item city.
            item_geo_georeferences = item.select_one(
                'div[class*="geo-georeferences-"]')
            if item_geo_georeferences:
                item_city = item_geo_georeferences.find('span').find(
                    'span').text
            else:
                item_city = None
            logger.warning(f'item_city:  {item_city}')

            # Getting an item publishing date.
            item_date_data = item.select_one(
                'div[data-marker="item-date"]').text
            # Convert '2 дня назад' or '5 минут назад' in normal calendar date.
            item_date = convert_date(item_date_data)
            # Remove the fractional part of the seconds after the dot and make
            # date as string just in case for SQLite
            item_date_list = str(item_date).split('.')
            item_date_str = item_date_list[0]
            # Getting a timestamp just in case
            item_date_timestamp = datetime.timestamp(item_date)
            logger.warning(f'item_date:  {item_date}')
        except Exception as err:
            logging.exception('Exception occurred')
            continue
        # data writing into a dictionary.
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
        # Put data dictionary as 'value' in new dictionary
        # with item_id as 'key'.
        data[item_id] = item_dict
        logger.warning(
            '##############################################################')
    logger.warning(f'items: {len(data)}')
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
        logger.warning(e)
        load_time = "Loading Error"
    return load_time
