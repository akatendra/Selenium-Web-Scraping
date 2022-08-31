import requests
from bs4 import BeautifulSoup

# DOES NOT WORK FOR AVITO.RU!!! SHOW PAGE STATUS CODE 403: FORBIDDEN #
URL = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/vtorichka'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
headers = {"user-agent": USER_AGENT}
page = requests.get(URL, headers=headers)
soup = None
page_status_code = page.status_code
print('page_status_code:', page_status_code)
if page_status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")
print(soup)
#print(soup)