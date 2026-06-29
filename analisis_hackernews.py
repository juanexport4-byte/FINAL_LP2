import json
from datetime import datetime, timezone
import re


# ── Palabras clave que sugieren contenido inauténtico / clickbait ─────────────
PALABRAS_ALERTA = [
    "guaranteed", "100%", "free money", "double your", "get rich",
    "passive income", "no risk", "pump", "winner", "claim now",
    "click here", "verify your", "suspended", "congratulations",
    "giveaway", "selected", "act now", "limited time", "DM me",
    "signal", "profit daily"
]

# Dominios de baja reputación conocidos por spam / contenido engañoso
DOMINIOS_SOSPECHOSOS = [
    "t.me", "bit.ly", "tinyurl", "cutt.ly", "rb.gy",
    "forms.", "form.", "survey", "click.", "earn.", "trade."
]


def calcular_sospecha_hn(post):
    """
    Señales adaptadas a los campos disponibles en Hacker News:
    texto (título), url, usuario, fecha_publicacion.
    """
    puntaje = 0
    señales = []

    texto = post.get("texto", "").lower()
    url   = post.get("url", "").lower()

    # Señal 1: título contiene palabras de alerta
    alertas_encontradas = [p for p in PALABRAS_ALERTA if p.lower() in texto]
    if alertas_encontradas:
        puntaje += 1
        señales.append("Título con lenguaje de alerta")

    # Señal 2: URL apunta a dominio sospechoso o acortador
    if any(d in url for d in DOMINIOS_SOSPECHOSOS):
        puntaje += 1
        señales.append("URL con dominio sospechoso o acortador")

    # Señal 3: URL de discusión interna de HN (sin fuente externa = sin respaldo)
    if "news.ycombinator.com/item" in url:
        puntaje += 1
        señales.append("Sin URL externa (solo discusión HN)")

    # Señal 4: publicación antigua (más de 3 años) reapareciendo en búsqueda
    fecha_str = post.get("fecha_publicacion", "")
    if fecha_str:
        try:
            fecha = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
            años = (datetime.now(timezone.utc) - fecha).days / 365
            if años > 3:
                puntaje += 1
                señales.append("Contenido con más de 3 años")
        except Exception:
            pass

    return puntaje, señales


def analizar_por_categoria(datos):
    por_categoria = {}
    for post in datos:
        cat = post["tipo_estafa"]
        por_categoria.setdefault(cat, []).append(post)

    resumen = {}

    for categoria, posts in por_categoria.items():
        total        = len(posts)
        sospechosos  = 0
        todas_señales = []

        for post in posts:
            puntaje, señales = calcular_sospecha_hn(post)
            if puntaje >= 2:
                sospechosos += 1
            todas_señales.extend(señales)

        conteo_señales = {}
        for s in todas_señales:
            conteo_señales[s] = conteo_señales.get(s, 0) + 1

        resumen[categoria] = {
            "total_posts":            total,
            "total_sospechosos":      sospechosos,
            "porcentaje_sospechosos": round((sospechosos / total) * 100, 1) if total else 0,
            "señales_frecuentes":     conteo_señales
        }

        print(f"\n{categoria}:")
        print(f"  Posts analizados:  {total}")
        print(f"  Sospechosos (2+):  {sospechosos} ({resumen[categoria]['porcentaje_sospechosos']}%)")
        print(f"  Señales:           {conteo_señales}")

    return resumen


if __name__ == "__main__":
    with open("datos_hackernews.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    print(f"Posts cargados: {len(datos)}")
    resumen = analizar_por_categoria(datos)

    with open("analisis_hackernews.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    print("\nGuardado en analisis_hackernews.json")
