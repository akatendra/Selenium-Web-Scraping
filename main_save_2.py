from datetime import datetime
import time
import scraper
import xlsx
import database
import logging.config
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, wait
from random import randint


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


def run_process(URL, page_number, filename,browser):
    # Initialize web browser
    # browser = scraper.get_firefox_browser()
    # scraper.connect_to_page(browser, URL, page_number)
    # logger.debug(f'Browser for page {page_number} opened: {spent_time()}')
    sleeptime = randint(1, 5)
    time.sleep(sleeptime)
    logger.debug(
        '##################################################################')
    logger.debug(f'Scraping page #{page_number}...')
    logger.debug(
        '##################################################################')
    html = browser.page_source
    logger.debug(f'Page_source of page {page_number} received: {spent_time()}')
    output_data = scraper.parse_html_kvartiry_vtorichka(html)
    logger.debug(f'Output_data of page {page_number} received: {spent_time()}')
    xlsx.append_xlsx_file(output_data, filename, page_number)
    database.write_to_database(output_data)

    # Go to pagination bar to simulate human behavior
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    pagination_bar = browser.find_element(By.XPATH,
                                          '//div[@data-marker="pagination-button"]')
    browser.execute_script("arguments[0].scrollIntoView();", pagination_bar)

    # Close the browser to free up computer memory
    # browser.quit()
    # logger.debug(f'Browser for page {page_number} closed: {spent_time()}')

    current_url = browser.current_url
    logger.debug(f'Current URL in run_process: {current_url}')
    return current_url

if __name__ == "__main__":
    # Set up logging
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    # Set the values of auxiliary variables
    time_begin = start_time = time.time()
    URL = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/vtorichka'
    current_page = 1
    output_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f'data_store/avito_{output_timestamp}.xlsx'
    # End of value settings

    logger.info('Start...')

    # Initialize web browser
    browser = scraper.get_firefox_browser()

    # Make a connection
    scraper.connect_to_page(browser, URL, current_page)

    current_url = run_process(URL, current_page, output_filename, browser)

    current_page = 2
    last_page = 100
    page_batch = 10

    while current_page <= last_page:
        logger.debug(f'Take in work page: {current_page}')
        page_url = f'{current_url}?p={current_page}'
        browser.get(page_url)
        run_process(current_url, current_page, output_filename, browser)
        current_page += 1


    # # Не работает!!! Такое ощущение что сервер банит
    # # Going through the pages and gathering the information we need
    # while current_page <= last_page:
    #     for _ in range(page_batch):
    #         if current_page <= last_page:
    #             run_process(current_url, current_page, output_filename, browser)
    #             logger.debug(f'Take in work page: {current_page}')
    #             current_page += 1
    #         else:
    #             break
    #         current_page += 1
    #
    #
    #
    #
    # # Multithreading не работает!!! Такое ощущение что сервер банит
    # # Adding multithreading
    # futures = []
    # with ThreadPoolExecutor() as executor:
    #     while current_page <= last_page:
    #         for _ in range(page_batch):
    #             if current_page <= last_page:
    #                 futures.append(executor.submit(run_process, current_url, current_page, output_filename))
    #                 logger.debug(f'ThreadPoolExecutor take in work page: {current_page}')
    #             else:
    #                 break
    #             current_page += 1
    #         # Wait for ending of all running processes
    #         wait(futures)
    #         # Clear list of running processes
    #         futures.clear()
    #         logger.debug(f'ThreadPoolExecutor finished processing a batch of pages. Current page: {current_page}')
    #
    # # Wait for ending of all running processes
    # wait(futures)
    # # End of multithreading

    # Stop script
    browser.quit()
    time_end = time.time()
    elapsed_time = time_end - time_begin
    if elapsed_time > 60:
        elapsed_minutes = elapsed_time // 60
        elapsed_sec = elapsed_time % 60
        elapsed_time_str = f'| {int(elapsed_minutes)} min {round(elapsed_sec, 1)} sec'
    else:
        elapsed_time_str = f'| {round(elapsed_time, 1)} sec'
    logger.info(f'Elapsed run time: {elapsed_time_str} seconds')