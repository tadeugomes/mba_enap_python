import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    # URL base do site de citações
    base_url = "https://quotes.toscrape.com/"
    # Lista para armazenar todas as citações coletadas
    quotes_data = []
    # Contador de páginas
    page = 1
    
    # Loop infinito para percorrer todas as páginas
    while True:
        # Monta a URL da página atual (primeira página não tem /page/1/)
        url = f"{base_url}page/{page}/" if page > 1 else base_url
        # Faz a requisição HTTP para obter o conteúdo da página
        response = requests.get(url)
        
        # Se a resposta não for bem sucedida (código 200), encerra o loop
        if response.status_code != 200:
            break
            
        # Cria um objeto BeautifulSoup para parsear o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # Encontra todos os elementos div com classe 'quote'
        quote_elements = soup.find_all('div', class_='quote')
        
        # Se não encontrar citações na página, encerra o loop
        if not quote_elements:
            break
            
        # Itera sobre cada elemento de citação encontrado
        for quote_element in quote_elements:
            # Extrai o texto da citação (span com classe 'text')
            quote_text = quote_element.find('span', class_='text').get_text(strip=True)
            # Extrai o nome do autor (small com classe 'author')
            author = quote_element.find('small', class_='author').get_text(strip=True)
            # Extrai todas as tags (links com classe 'tag') e cria uma lista
            tags = [tag.get_text(strip=True) for tag in quote_element.find_all('a', class_='tag')]
            
            # Adiciona os dados da citação à lista como um dicionário
            quotes_data.append({
                'quote': quote_text,
                'author': author,
                'tags': tags
            })
        
        # Verifica se existe botão "Próxima →" para navegar para próxima página
        next_button = soup.find('li', class_='next')
        # Se não houver botão de próxima página, encerra o loop
        if not next_button:
            break
            
        # Incrementa o número da página
        page += 1
    
    # Retorna a lista completa de citações
    return quotes_data

# Bloco principal que executa quando o script é rodado diretamente
if __name__ == "__main__":
    # Chama a função para coletar as citações
    quotes = scrape_quotes()
    
    # Abre o arquivo quotes.txt em modo de escrita com codificação UTF-8
    with open('quotes.txt', 'w', encoding='utf-8') as f:
        # Itera sobre as citações com numeração começando em 1
        for i, quote in enumerate(quotes, 1):
            # Escreve o número da citação
            f.write(f"Citação {i}:\n")
            # Escreve o texto da citação
            f.write(f"Quote: {quote['quote']}\n")
            # Escreve o autor
            f.write(f"Author: {quote['author']}\n")
            # Escreve as tags separadas por vírgula
            f.write(f"Tags: {', '.join(quote['tags'])}\n")
            # Escreve uma linha separadora
            f.write("-" * 50 + "\n")
    
    # Imprime mensagem de sucesso com o total de citações coletadas
    print(f"Coletadas {len(quotes)} citações e salvas em quotes.txt")