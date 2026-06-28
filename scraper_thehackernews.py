import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

def extraer_noticias_estafas(termino_busqueda, categoria, limite=5):
    print(f"Buscando en la web: {categoria} ({termino_busqueda})...")
    
    # URL de búsqueda de The Hacker News
    url = f"https://thehackernews.com/search?q={termino_busqueda}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articulos = soup.find_all('div', class_='body-post', limit=limite)
    
    resultados = []
    
    for articulo in articulos:
        # Extracción de elementos con BeautifulSoup
        titulo_tag = articulo.find('h2', class_='home-title')
        enlace_tag = articulo.find('a', class_='story-link')
        fecha_tag = articulo.find('div', class_='item-label')
        resumen_tag = articulo.find('div', class_='home-desc')
        
        if titulo_tag and enlace_tag:
            titulo = titulo_tag.text.strip()
            url_post = enlace_tag['href']
            
            # Limpieza de texto y fecha
            texto = resumen_tag.text.strip() if resumen_tag else "Sin descripción"
            fecha_pub = fecha_tag.text.split('')[1].strip() if fecha_tag and '' in fecha_tag.text else datetime.now().strftime("%Y-%m-%d")
            
            resultados.append({
                "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
                "fecha_publicacion": fecha_pub,
                "tipo_estafa": categoria,
                "fuente": "The Hacker News",
                "usuario": "Autor de Artículo Web",
                "texto": f"{titulo} - {texto}",
                "url": url_post
            })
            
    return resultados

if __name__ == "__main__":
    categorias = {
        "Criptomonedas": "crypto scam AI",
        "Phishing": "phishing LLM",
        "Inversiones": "investment fraud",
        "Suplantación": "impersonation deepfake"
    }

    todos_los_datos = []

    for categoria, termino in categorias.items():
        resultados = extraer_noticias_estafas(termino, categoria, limite=5)
        todos_los_datos.extend(resultados)
        time.sleep(2) 

    print(f"\nArtículos extraídos: {len(todos_los_datos)}")

    # Guardado en JSON
    with open("datos_thehackernews.json", "w", encoding="utf-8") as f:
        json.dump(todos_los_datos, f, ensure_ascii=False, indent=4)

    print("Guardado")
