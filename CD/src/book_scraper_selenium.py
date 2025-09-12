import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_books_with_selenium():
    """
    Realiza o web scraping de todos os livros do site http://books.toscrape.com/
    utilizando Selenium para navegação e coleta de dados.

    Coleta título, preço e o link para a página de detalhes de cada livro, navegando
    por todas as páginas de listagem.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um livro
              e contém as chaves 'titulo', 'preco' e 'link'.
    """
    # Configura o WebDriver do Chrome automaticamente
    # Adiciona opções para rodar em modo 'headless' (sem abrir a janela do navegador)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    start_url = "http://books.toscrape.com/"
    driver.get(start_url)

    all_books = []
    print("Iniciando o scraping de livros com Selenium...")

    while True:
        print(f"Coletando dados de: {driver.current_url}")

        # Encontra todos os 'articles' que representam um livro na página
        books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')

        for book in books:
            # Extrai o título do atributo 'title' da tag 'a' dentro do 'h3'
            title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')

            # Extrai o preço do texto da tag 'p' com a classe 'price_color'
            price = book.find_element(By.CSS_SELECTOR, '.price_color').text

            # Constrói o link absoluto para a página do livro
            link = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('href')

            all_books.append({
                'titulo': title,
                'preco': price,
                'link': link
            })

        # Tenta encontrar e clicar no botão 'next'
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
            next_button.click()
            # Aguarda até que a lista de livros da próxima página seja carregada
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article.product_pod'))
            )
        except NoSuchElementException:
            # Se não houver um botão 'next', chegamos à última página
            print("Não há mais páginas para navegar.")
            break

    driver.quit()
    print("\nScraping finalizado!")
    return all_books

if __name__ == '__main__':
    scrape_books_with_selenium()

    if scraped_data:
        print(f"\nTotal de livros coletados: {len(scraped_data)}")
        print("\nAmostra dos dados coletados (primeiros 5 livros):")
        for item in scraped_data[:5]:
            print(item)
    else:
        print("Nenhum dado foi coletado.")
