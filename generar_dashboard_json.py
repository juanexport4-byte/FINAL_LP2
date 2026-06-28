import json
from collections import Counter

# Cargar ambas fuentes
with open("datos_bluesky.json", "r", encoding="utf-8") as f:
    posts_bluesky = json.load(f)

with open("datos_hackernews.json", "r", encoding="utf-8") as f:
    posts_hackernews = json.load(f)