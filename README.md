# 🏛️ Statesota Moral Center

> «Aprende tu lección antes de que tu padre vaya al estudio»

Aplicación web con temática inspirada en **Moral Orel** que combina scraping de citas, procesamiento de lenguaje natural y generación de texto para ofrecer tres experiencias interactivas: un buscador semántico de citas, un generador de ensayos/sermones apologéticos y un simulador de empaquetado y traducción de peticiones por lotes.

## ✨ Funcionalidades

### 1. Buscador Semántico de Culpas y Vibras
El usuario describe una situación o estado emocional en lenguaje libre. El texto se traduce automáticamente al inglés y se compara mediante **similitud coseno sobre vectores TF-IDF** contra el corpus de citas, devolviendo las 3 más afines junto a su porcentaje de afinidad.

### 2. El Polemista Devoto
A partir de un tema o pregunta, genera un ensayo académico estructurado de 6 párrafos (introducción, 4 párrafos de desarrollo y conclusión), incrustando una cita relacionada semánticamente mediante un mapa de conceptos español→inglés y evitando repetir citas ya usadas en la sesión.

### 3. Empaquetador de Tokens y Traductor
Simula la lógica de *batching* que usaría un pipeline de traducción o de llamadas a una API con límite de caracteres: agrupa las citas en lotes según un límite configurable de caracteres por petición y muestra el desglose resultante.

## 🛠️ Tecnologías y decisiones técnicas

| Capa | Tecnología | Motivo |
|---|---|---|
| Backend | **Flask** | Servidor ligero para exponer las 3 rutas de API y servir la plantilla HTML |
| Scraping | **BeautifulSoup4 + requests** | Extracción de citas y autores desde `quotes.toscrape.com`, paginando hasta un límite práctico de 30 citas |
| NLP / Similitud | **scikit-learn** (`TfidfVectorizer` + `cosine_similarity`) | Vectorización por n-gramas de caracteres (`char_wb`, 3-5) para tolerar variaciones léxicas al comparar texto traducido contra las citas originales en inglés |
| Traducción | **deep-translator (GoogleTranslator)** | Traducción español↔inglés tanto de las citas cacheadas como del texto que ingresa el usuario |
| Datos | **pandas** | Manejo tabular del corpus de citas (`df_citas`) para las operaciones de vectorización y empaquetado |
| Cache | `citas_cache.json` | Evita repetir el scraping y la traducción en cada arranque; si el archivo existe y tiene contenido, se reutiliza |
| Frontend | **HTML5 + CSS3 + JavaScript vanilla (ES6)** | Sin frameworks; navegación por pestañas con `fetch` async hacia la API Flask, siguiendo un enfoque minimalista y directo |
| Tipografía | Google Fonts (`Cinzel`, `Metamorphous`, `Old Standard TT`) | Refuerzan la estética gótico-eclesiástica del tema Moral Orel |

**Decisiones de diseño relevantes:**
- El scraping tiene un **fallback** con citas fijas si la petición a `quotes.toscrape.com` falla, garantizando que la app nunca quede sin datos.
- El vectorizador usa n-gramas de caracteres en lugar de palabras completas, lo que hace la búsqueda más robusta ante traducciones imperfectas del texto del usuario.
- El historial de citas usadas (`historial_indices`) evita que el Polemista repita la misma cita en sesiones consecutivas, reiniciándose cuando se agotan las disponibles.

## 📂 Estructura del proyecto

```
.
├── app.py                  # Backend Flask: scraping, NLP, generación de ensayos, empaquetado
├── requirements.txt        # Dependencias de Python
├── citas_cache.json        # Cache de citas ya scrapeadas y traducidas
├── templates/
│   └── index.html          # Vista principal con las 3 pestañas
└── static/
    ├── css/
    │   └── style.css        # Estilos con temática gótico-eclesiástica
    └── js/
        └── moral.js         # Lógica de pestañas y llamadas fetch a la API
```

> ⚠️ Nota: `index.html` referencia `static/css/style.css` y `static/js/moral.js` mediante `url_for`, por lo que estos archivos deben ubicarse dentro de las carpetas `templates/` y `static/` respectivamente para que Flask los sirva correctamente.

## 🚀 Cómo ejecutarlo

### Requisitos previos
- Python 3.9+
- pip

### Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd <nombre-del-proyecto>

# 2. Crear un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
python app.py
```

La aplicación quedará disponible en `http://localhost:5000`.

> La primera vez que se ejecute, si no existe `citas_cache.json` con datos, la app hará scraping en vivo de `quotes.toscrape.com` y traducirá las citas al español, lo cual puede tardar unos segundos.

## 📡 Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/vibras` | Recibe `{ "situacion": "..." }` y devuelve las 3 citas más afines semánticamente |
| `POST` | `/api/polemista` (alias `/generar`) | Recibe `{ "pregunta": "..." }` y devuelve un ensayo de 6 párrafos con cita incrustada |
| `POST` | `/api/empaquetador` | Recibe `{ "max_units": 200 }` y devuelve el desglose de lotes de citas agrupadas por límite de caracteres |

## 📦 Dependencias (`requirements.txt`)

```
flask==3.0.2
requests==2.31.0
beautifulsoup4==4.12.3
scikit-learn==1.4.1.post1
pandas==2.2.1
deep-translator==1.11.4
```

## ⚖️ Fuente de datos

Las citas se obtienen de [quotes.toscrape.com](https://quotes.toscrape.com), un sitio público diseñado específicamente para practicar técnicas de web scraping.

## 👤 Autor

**Diego** — Desarrollador web en formación, enfocado en frontend y JavaScript vanilla.
GitHub: [Dieg0Rgu](https://github.com/Dieg0Rgu)

## 📄 Licencia

Proyecto con fines educativos.
