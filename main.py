from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
# Unable to hide "Chrome is being controlled by automated software" infobar
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
# Open Chrome for full size of screen
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--disable-extensions') #  ?
#  Цill launch browser without UI(headless)
# chrome_options.add_argument('--headless')
CHROME_PATH = 'd:\Python\chromedriver_win32\chromedriver.exe'
service = Service(CHROME_PATH)
browser = webdriver.Chrome(service=service, options=chrome_options)
URL = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/vtorichka'
browser.get(URL)
