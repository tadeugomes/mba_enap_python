from __future__ import annotations

import time
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def _setup_driver() -> webdriver.Chrome:
    """Initialize a headless Chrome WebDriver.

    Returns
    -------
    webdriver.Chrome
        A configured Selenium WebDriver instance running Chrome in headless
        mode.  Adjust the options here if you need a visible browser window
        during debugging.
    """
    options = webdriver.ChromeOptions()
    # Run in headless mode so the browser window does not pop up.
    options.add_argument("--headless=new")
    # These options help Selenium run more reliably in containerised
    # environments.
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # Increase window size to ensure all elements are within view.
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


if __name__ == '__main__':
    driver = _setup_driver()
    url = 'http://books.toscrape.com/'
    driver.get(url)
    lista = []
    while True:
        lista_divs = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')
        for d in lista_divs:
            url_img = d.find_element(By.XPATH, './div/a/img').get_attribute('src')
            price = float(d.find_element(By.XPATH, './div/p[@class="price_color"]').text[1:])
            title = d.find_element(By.XPATH, './h3/a').text
            registro = {
                'url_img': url_img,
                'price': price,
                'title': title
            }
            lista.append(registro)

        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="next"]/a')
            next_button.click()
        except NoSuchElementException:
            break

    driver.quit()
        

    print(lista)
