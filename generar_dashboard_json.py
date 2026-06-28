import json
from collections import Counter

# Cargar ambas fuentes
with open("datos_bluesky.json", "r", encoding="utf-8") as f:
    posts_bluesky = json.load(f)

with open("datos_hackernews.json", "r", encoding="utf-8") as f:
    posts_hackernews = json.load(f)


def contar_por_categoria(posts):
    conteo = Counter(post["tipo_estafa"] for post in posts)
    conteo_ordenado = conteo.most_common()
    etiquetas = [item[0] for item in conteo_ordenado]
    valores = [item[1] for item in conteo_ordenado]
    return etiquetas, valores


# Conteos individuales por plataforma
etiquetas_bsky, valores_bsky = contar_por_categoria(posts_bluesky)
etiquetas_hn, valores_hn = contar_por_categoria(posts_hackernews)