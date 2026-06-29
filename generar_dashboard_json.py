import json
from collections import Counter

# ── Cargar datos de ambas fuentes ─────────────
with open("datos_bluesky.json", "r", encoding="utf-8") as f:
    posts_bluesky = json.load(f)

with open("datos_hackernews.json", "r", encoding="utf-8") as f:
    posts_hackernews = json.load(f)

# ── Cargar análisis ────────────────────────────
with open("analisis_bluesky.json", "r", encoding="utf-8") as f:
    analisis_bluesky = json.load(f)

with open("analisis_hackernews.json", "r", encoding="utf-8") as f:
    analisis_hackernews = json.load(f)


def contar_por_categoria(posts):
    conteo = Counter(post["tipo_estafa"] for post in posts)
    conteo_ordenado = conteo.most_common()
    return [i[0] for i in conteo_ordenado], [i[1] for i in conteo_ordenado]


def resumir_analisis(analisis):
    return {
        categoria: {
            "total_posts":            data["total_posts"],
            "total_sospechosos":      data["total_sospechosos"],
            "porcentaje_sospechosos": data["porcentaje_sospechosos"],
            "señales_frecuentes":     data["señales_frecuentes"]
        }
        for categoria, data in analisis.items()
    }


etiquetas_bsky, valores_bsky = contar_por_categoria(posts_bluesky)
etiquetas_hn,   valores_hn   = contar_por_categoria(posts_hackernews)

todos_los_posts = posts_bluesky + posts_hackernews

tabla = [
    {
        "fecha":  post["fecha_extraccion"],
        "estafa": post["tipo_estafa"],
        "fuente": post["fuente"],
        "url":    post["url"]
    }
    for post in todos_los_posts
]

datos_dashboard = {
    "bluesky": {
        "etiquetas": etiquetas_bsky,
        "valores":   valores_bsky,
        "analisis":  resumir_analisis(analisis_bluesky)
    },
    "fuente2": {
        "nombre":    "Hacker News",
        "etiquetas": etiquetas_hn,
        "valores":   valores_hn,
        "analisis":  resumir_analisis(analisis_hackernews)
    },
    "tabla": tabla
}

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos_dashboard, f, ensure_ascii=False, indent=2)

print(f"datos.json generado con {len(todos_los_posts)} posts en total")
print(f"Análisis Bluesky:      {len(analisis_bluesky)} categorías")
print(f"Análisis Hacker News:  {len(analisis_hackernews)} categorías")
