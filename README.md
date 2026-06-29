# El uso de LLMs en las estafas 

## Integrantes del Grupo
* **20241372	Aguilar Farfán, Juan Fernando** - [@juanexport4-byte](https://github.com/juanexport4-byte)
* **20241384	Guevara Alvarado, Samuel Christian** - [@chrissg05](https://github.com/chrissg05)
* **20241392	Pacheco Pampas, Merly Vanessa** - [@Nessa22123](https://github.com/Nessa22123)
* **20240733	Salazar Vasquéz, Ytzel Aleeza** - [@ytzelsalazar](https://github.com/ytzelsalazar)

## 🌐 Dashboard en vivo

🔗 [Ver dashboard](https://proyectofinallp2.netlify.app/)

---

## Descripción del proyecto

Este proyecto investiga cómo la desinformación y el fraude en redes sociales se han vuelto más difíciles de controlar, en parte porque los LLMs abaratan la generación de contenido falso .

El sistema recopila publicaciones relacionadas a cinco categorías de estafa (criptomonedas, phishing, inversiones, sorteos falsos y suplantación) desde dos fuentes públicas — **Bluesky** y **Hacker News** — y analiza señales de comportamiento inauténtico como cuentas nuevas con pocos seguidores, similitud textual entre cuentas distintas, y lenguaje típico de estafadores.

El resultado es un **dashboard interactivo** que permite explorar los datos recolectados, ver el análisis por categoría y plataforma, y acceder a los posts originales.

---

## Estructura del proyecto

```
├── index.html                   # Dashboard interactivo principal
├── script.js                    # Lógica de gráficos e interacciones (Chart.js)
├── css/
│   └── styles.css               # Estilos del dashboard 
│
├── scraper_bluesky.py           # Extrae posts de Bluesky vía API oficial (atproto)
├── scraper_hackernews.py        # Extrae posts de Hacker News vía API pública de Algolia
├── obtener_perfiles_bluesky.py  # Para obtener datos de perfil públicos de cada cuenta (seguidores,seguidos,antidad_posts,descripcion,fecha_creacion y verificado) para analizar si es generado por un posbiel LLM
├── analisis_bluesky.py          # Analiza señales de sospecha en cuentas de Bluesky
├── analisis_hackernews.py       # Analiza señales de sospecha en posts de Hacker News
├── generar_dashboard_json.py    # Combina todos los datos y genera datos.json para el dashboard
│
├── datos_bluesky.json           # Posts extraídos de Bluesky (generado por scraper_bluesky.py)
├── datos_hackernews.json        # Posts extraídos de Hacker News (generado por scraper_hackernews.py)
├── datos_cuenta_bluesky.json    # Posts de Bluesky con datos de perfil públicos de cada cuenta para analizar si es generado por un LLM
├── analisis_bluesky.json        # Resultados del análisis de sospecha por categoría en Bluesky
├── analisis_hackernews.json     # Resultados del análisis de sospecha por categoría en Hacker News
├── datos.json                   # JSON final combinado que usa el dashboard (generado automáticamente)
│
└── README.md                    # Este archivo
```

---

## Pipeline del sistema

```
scraper_bluesky.py
        │
        ▼
datos_bluesky.json ──► obtener_perfiles_bluesky.py ──► datos_cuenta_bluesky.json ──► analisis_bluesky.py ──► analisis_bluesky.json
                                                                                                                        │
scraper_hackernews.py                                                                                                   │
        │                                                                                                               │
        ▼                                                                                                               │
datos_hackernews.json ──► analisis_hackernews.py ──► analisis_hackernews.json                                          │
                                                              │                                                         │
                                                              └──────────────────► generar_dashboard_json.py ◄──────────┘
                                                                                            │
                                                                                            ▼
                                                                                       datos.json
                                                                                            │
                                                                                            ▼
                                                                                    index.html (dashboard)
```

---

## Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install atproto requests beautifulsoup4
```

### 2. Configurar credenciales de Bluesky

En `scraper_bluesky.py` y `obtener_perfiles_bluesky.py`, reemplaza:
```python
obtener_perfiles("tu_usuario.bsky.social", "tu_app_password")
```

Para obtener tu `app_password`: Bluesky → Configuración → Privacidad y seguridad → Contraseñas de aplicación.

### 3. Ejecutar en orden

```bash
# Paso 1: Extraer datos
python scraper_bluesky.py
python scraper_hackernews.py

# Paso 2: Enriquecer con datos de perfil (solo Bluesky)
python obtener_perfiles_bluesky.py

# Paso 3: Analizar señales de sospecha
python analisis_bluesky.py
python analisis_hackernews.py

# Paso 4: Generar datos.json para el dashboard
python generar_dashboard_json.py
```

### 4. Para ver el dashboard localmente

```bash
python -m http.server 5500
```

Luego abrir  `http://localhost:5500` en su navegador.

---

## Fuentes de datos

| Fuente | Tipo de acceso | robots.txt | Contenido |
|--------|---------------|------------|-----------|
| **Bluesky** | API oficial SDK `atproto` | Permitido vía API oficial | Posts directos de usuarios, posibles estafadores activos |
| **Hacker News** | API pública Algolia (`hn.algolia.com/api/v1/search`) | Permitido sin restricciones | Discusión comunitaria técnica sobre casos de fraude |

---

##  Análisis de señales de sospecha

### Bluesky (`analisis_bluesky.py`)
Analiza datos de perfil de cada cuenta para detectar comportamiento inauténtico:

| Señal | Criterio |
|-------|----------|
| Pocos seguidores | Menos de 50 seguidores |
| Ratio seguidos/seguidores alto | Ratio > 5 (sigue a muchos, pocos lo siguen) |
| Cuenta reciente | Creada hace menos de 6 meses |
| Sin descripción de perfil | Campo de descripción vacío |

Una cuenta con **2 o más señales** se clasifica como sospechosa.

### Hacker News (`analisis_hackernews.py`)
Como no hay datos de perfil disponibles, el análisis se basa en el contenido del post:

| Señal | Criterio |
|-------|----------|
| Lenguaje de alerta | Título contiene términos típicos de estafa ("guaranteed", "free money", "DM me", etc.) |
| URL sospechosa | Enlace a acortadores o dominios de baja reputación (t.me, bit.ly, etc.) |
| Sin URL externa | Solo enlace interno de HN, sin fuente externa que respalde el contenido |
| Contenido antiguo | Publicado hace más de 3 años |

---

## Consideraciones éticas

- Solo se extrae información **públicamente visible** — no se accede a datos privados ni mensajes directos
- Ambas fuentes fueron verificadas en sus `robots.txt` antes del uso
- Se respetan límites de peticiones con pausas entre requests (`time.sleep`)
- Los datos se usan exclusivamente con fines de investigación académica
- Hacker News indica `ai-train=no` en su robots.txt — el contenido no se usa para entrenar modelos

---

## Informe

📎 [Ver informe completo](https://docs.google.com/document/d/1OzFwKaldOoGCvyCMHulLMKlCoXUIpwLp/edit?usp=sharing&ouid=106838032057067217145&rtpof=true&sd=true)
