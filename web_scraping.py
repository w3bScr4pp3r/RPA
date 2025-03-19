import requests
from bs4 import BeautifulSoup
import time

def scrape_wikipedia(article_title=None, url=None, paragraphs=3):
    """
    Extrai conteúdo de um artigo da Wikipedia.
    
    Args:
        article_title (str): Título do artigo (opcional se URL for fornecido)
        url (str): URL completa do artigo (opcional se title for fornecido)
        paragraphs (int): Número de parágrafos para extrair (0 para todos)
    
    Returns:
        str: Conteúdo extraído ou mensagem de erro
    """
    # Construir URL se não for fornecida
    if not url:
        if not article_title:
            return "Erro: Forneça um título ou URL do artigo"
        url = f"https://pt.wikipedia.org/wiki/{article_title.replace(' ', '_')}"
    
    # Configurar headers para simular navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        # Fazer requisição
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Verificar se a página existe
        if response.url == "https://pt.wikipedia.org/wiki/Main_Page":
            return "Erro: Artigo não encontrado"
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar conteúdo principal
        content = soup.find('div', {'id': 'mw-content-text'})
        
        # Extrair parágrafos
        paragraphs_list = []
        for p in content.find_all('p'):
            text = p.get_text().strip()
            if text:
                paragraphs_list.append(text)
        
        # Selecionar número de parágrafos
        if paragraphs == 0:
            result = '\n\n'.join(paragraphs_list)
        else:
            result = '\n\n'.join(paragraphs_list[:paragraphs])
        
        return result
    
    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {str(e)}"
    
    finally:
        # Respeitar política de acesso
        time.sleep(1)

# Exemplo de uso
if __name__ == "__main__":
    # Buscar artigo sobre Python (linguagem de programação)
    texto_a_ser_pesquisado = input("Digite o texto a ser pesquisado: ")
    content = scrape_wikipedia(article_title=texto_a_ser_pesquisado, paragraphs=0)
    # Verificar se ocorreu algum erro
    if not content.startswith("Erro"):
        print("Conteúdo encontrado:\n")
        print(content)
    else:
        print(content)
