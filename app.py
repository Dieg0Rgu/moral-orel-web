import json
import os
import random
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from flask import Flask, jsonify, render_template, request
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

JSON_FILE = "citas_cache.json"

# --- MÓDULO DE SCRAPING Y TRADUCCIÓN ---

def cargar_o_extraer_citas():
    """Extrae o lee citas y garantiza su traducción al español mediante deep-translator."""
    citas_extraidas = []

    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                citas_extraidas = json.load(f)
        except Exception as e:
            print(f"Error al leer caché: {e}")

    if not citas_extraidas:
        BASE_URL = "https://quotes.toscrape.com"
        ruta_actual = "/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        }

        try:
            while ruta_actual and len(citas_extraidas) < 30:  # Límite práctico
                res = requests.get(
                    f"{BASE_URL}{ruta_actual}", headers=headers, timeout=10
                )
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "html.parser")

                for bloque in soup.find_all("div", class_="quote"):
                    txt = bloque.find("span", class_="text")
                    aut = bloque.find("small", class_="author")
                    if txt and aut:
                        citas_extraidas.append({
                            "cita_en": txt.get_text().strip("“”\"' "),
                            "autor": aut.get_text().strip(),
                        })

                next_btn = soup.find("li", class_="next")
                ruta_actual = (
                    next_btn.find("a")["href"]
                    if next_btn and next_btn.find("a")
                    else None
                )

        except Exception as e:
            print(f"Error durante el scraping: {e}")
            citas_extraidas = [
                {
                    "cita_en": (
                        "It is our choices, Harry, that show what we truly are, far"
                        " more than our abilities."
                    ),
                    "autor": "J.K. Rowling",
                },
                {
                    "cita_en": (
                        "The world as we have created it is a process of our"
                        " thinking. It cannot be changed without changing our thinking."
                    ),
                    "autor": "Albert Einstein",
                },
                {
                    "cita_en": (
                        "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid."
                    ),
                    "autor": "Jane Austen",
                }
            ]

        # Traducción al español usando deep-translator
        translator = GoogleTranslator(source="en", target="es")
        for item in citas_extraidas:
            try:
                item["cita_es"] = translator.translate(item["cita_en"])
            except Exception:
                item["cita_es"] = item["cita_en"]

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(citas_extraidas, f, ensure_ascii=False, indent=4)

    return citas_extraidas


citas_data = cargar_o_extraer_citas()
df_citas = pd.DataFrame(citas_data)

# Vectorizador TF-IDF para el buscador de vibras
vectorizer = TfidfVectorizer(
    analyzer="char_wb", ngram_range=(3, 5), lowercase=True
)
matrices_citas = vectorizer.fit_transform(df_citas["cita_en"])


# --- LÓGICA DE POLEMISTA (ENSAYO EXTENSO DE 6 PÁRRAFOS) ---

MAPA_CONCEPTOS = {
    "mundo": "world", "cambiar": "change", "pensar": "thinking", "pensamiento": "thinking",
    "elegir": "choice", "eleccion": "choices", "opcion": "choices", "habilidad": "abilities",
    "vida": "live", "vivir": "life", "milagro": "miracle", "magia": "miracle",
    "novela": "novel", "libro": "novel", "literatura": "novel", "exito": "success",
    "triunfo": "success", "valor": "value", "fracaso": "failed", "fracasar": "failed",
    "verdad": "truth", "amor": "love", "tiempo": "time", "muerte": "death",
    "educacion": "thinking", "ejercicio": "life", "salud": "life", "mente": "thinking"
}

historial_indices = []

def buscar_cita_afin(tema: str):
    """Busca una cita semánticamente relacionada en la BD o rota entre las disponibles."""
    global historial_indices
    query_limpia = re.sub(r'[^\w\s]', '', tema.lower())
    palabras = query_limpia.split()

    for palabra in palabras:
        if palabra in MAPA_CONCEPTOS:
            concepto_en = MAPA_CONCEPTOS[palabra]
            for idx, item in enumerate(citas_data):
                if concepto_en in item['cita_en'].lower() and idx not in historial_indices:
                    historial_indices.append(idx)
                    return item

    indices_disponibles = [i for i in range(len(citas_data)) if i not in historial_indices]
    if not indices_disponibles:
        historial_indices.clear()
        indices_disponibles = list(range(len(citas_data)))
        
    elegido_idx = random.choice(indices_disponibles)
    historial_indices.append(elegido_idx)
    return citas_data[elegido_idx]


def generar_ensayo_6_parrafos(pregunta: str) -> dict:
    """Construye un ensayo de 6 párrafos basado en la estructura académica formal."""
    tema_limpio = pregunta.strip("¿? ‽ ").capitalize()
    
    cita_item = buscar_cita_afin(tema_limpio)
    autor = cita_item["autor"]
    cita_en = cita_item["cita_en"]
    cita_es = cita_item.get("cita_es", cita_en)
    
    cita_bloque = f'"{cita_en}" (Traducido al español: "{cita_es}")'

    # PÁRRAFO 1: INTRODUCCIÓN
    p1_intro = (
        f"El tema relativo a '{tema_limpio}' es una cuestión fundamental que ha estado presente "
        f"en la reflexión humana desde tiempos inmemoriales. A lo largo de la historia, este fenómeno "
        f"ha sido examinado desde diversas perspectivas teóricas y empíricas, pero hoy en día descubrimos "
        f"cada vez más su impacto directo en la estructura de nuestro desarrollo social e individual. "
        f"En esta era de transformaciones aceleradas y dilemas crecientes, resulta imprescindible explorar cómo "
        f"las dinámicas asociadas a este ámbito pueden constituir una herramienta eficaz para transformar nuestra realidad. "
        f"Este ensayo analizará de manera rigurosa el vínculo entre el planteamiento expuesto y sus implicaciones prácticas, "
        f"destacando la necesidad e importancia de integrar este análisis crítico en nuestra vida cotidiana."
    )

    # PÁRRAFOS 2 AL 5: DESARROLLO
    p2_desarrollo = (
        f"En primer lugar, '{tema_limpio}' genera numerosos efectos beneficiosos e indispensables para el entendimiento integral. "
        f"Al descomponer sus premisas esenciales, se libera una perspectiva analítica que actúa como un catalizador natural "
        f"de juicio crítico, generando una profunda sensación de claridad conceptual e intelectual. Esto resulta especialmente "
        f"útil para abordar los dilemas contemporáneos, ya que permite reducir la incertidumbre y mitigar los sesgos preconcebidos, "
        f"fortaleciendo la capacidad reflexiva de los individuos frente a escenarios de alta complejidad."
    )

    p3_desarrollo = (
        f"Además, el examen constante de esta materia contribuye de manera significativa a regular las tensiones éticas e "
        f"ideológicas de la sociedad. Cuando nos enfrentamos a controversias o situaciones estresantes dentro del debate público, "
        f"el rigor analítico ayuda a modular las respuestas impulsivas. Es precisamente en este marco reflexivo donde la contribución "
        f"de {autor} cobra una fuerza extraordinaria. En su obra se destaca una premisa esclarecedora: {cita_bloque}. "
        f"Esta reflexión demuestra que una aproximación metodológica adecuada permite disminuir la fricción conceptual y afianzar la coherencia argumentativa."
    )

    p4_desarrollo = (
        f"El fundamento epistemológico es otro aspecto crucial en este debate, y la profundización en '{tema_limpio}' "
        f"desempeña un papel determinante en la consolidación del conocimiento duradero. Las comunidades que examinan esta "
        f"problemática con regularidad tienden a estructurar mejores soluciones y experimentan un grado sustancialmente menor de "
        f"errores sistemáticos. La continuidad en el estudio de este factor fortalece la resiliencia del pensamiento frente al estancamiento doctrinal."
    )

    p5_desarrollo = (
        f"Por último, este proceso promueve la autoestima intelectual y la confianza en la capacidad deductiva propia. "
        f"Al alcanzar metas de comprensión profunda y superar los desafíos analíticos implícitos en la discusión de '{tema_limpio}', "
        f"las personas pueden sentirse más empoderadas y satisfechas con su discernimiento y capacidad crítica. "
        f"Esto repercute de forma directa y positiva en la autonomía del pensamiento, optimizando el autoconcepto y la seguridad en la toma de decisiones."
    )

    # PÁRRAFO 6: CONCLUSIÓN
    p6_conclusion = (
        f"En resumen, la indagación sobre '{tema_limpio}' no solo es valiosa para la teoría abstracta, sino que tiene "
        f"un impacto significativo en la praxis humana. A través del fortalecimiento del juicio crítico, la reducción "
        f"del sesgo, la consolidación epistemológica y el desarrollo del empoderamiento personal, este enfoque se convierte en una "
        f"herramienta invaluable para abordar las paradojas del mundo moderno. Como sociedad, debemos promover activamente la importancia "
        f"de incorporar esta perspectiva analítica en nuestra rutina diaria para mantener no solo nuestro conocimiento actualizado, "
        f"sino también nuestra mente en óptimas condiciones."
    )

    # Texto continuo formateado para respuesta tradicional o despliegue directo
    ensayo_texto = f"{p1_intro}\n\n{p2_desarrollo}\n\n{p3_desarrollo}\n\n{p4_desarrollo}\n\n{p5_desarrollo}\n\n{p6_conclusion}"

    return {
        "titulo": f"El Impacto Reflexivo de '{tema_limpio}'",
        "intro": p1_intro,
        "desarrollo": [p2_desarrollo, p3_desarrollo, p4_desarrollo, p5_desarrollo],
        "conclusion": p6_conclusion,
        "ensayo": ensayo_texto,
        "cita_original": cita_en,
        "autor": autor
    }


# --- RUTAS DE LA APLICACIÓN ---

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/vibras", methods=["POST"])
def buscador_vibras():
    """Ejercicio 1: Buscador de Vibras por Similitud Semántica"""
    data = request.json or {}
    texto = data.get("situacion", "").strip()

    if len(texto) < 10:
        return jsonify({"error": "Por favor escribe al menos 10 caracteres."}), 400

    try:
        texto_en = GoogleTranslator(source="auto", target="en").translate(texto)
    except Exception:
        texto_en = texto

    matriz_usr = vectorizer.transform([texto_en])
    similitudes = cosine_similarity(matriz_usr, matrices_citas).flatten()
    top_indices = similitudes.argsort()[-3:][::-1]

    resultados = []
    for idx in top_indices:
        resultados.append({
            "cita_en": df_citas.iloc[idx]["cita_en"],
            "cita_es": df_citas.iloc[idx]["cita_es"],
            "autor": df_citas.iloc[idx]["autor"],
            "afinidad": f"{similitudes[idx]:.1%}",
        })

    return jsonify({"resultados": resultados})


@app.route("/api/polemista", methods=["POST"])
def polemista_debate():
    """Ejercicio 2: Generador de Ensayos Académicos de 6 Párrafos"""
    data = request.json or {}
    pregunta = data.get("pregunta", "").strip() or data.get("prompt", "").strip()

    if not pregunta:
        return jsonify({"error": "Ingresa una pregunta o tema válido."}), 400

    resultado = generar_ensayo_6_parrafos(pregunta)
    return jsonify(resultado)


@app.route("/generar", methods=["POST"])
def generar_alias():
    """Alias para la ruta /api/polemista para compatibilidad con el frontend."""
    return polemista_debate()


@app.route("/api/empaquetador", methods=["POST"])
def empaquetar_y_traducir():
    """Ejercicio 3: Presupuesto, Empaquetado dinámico por tokens y Traducción"""
    data = request.json or {}
    max_units = int(data.get("max_units", 200))

    lotes = []
    lote_actual = []
    tamano_actual = 0

    for idx, row in df_citas.iterrows():
        texto = row["cita_en"]
        tamano = len(texto)

        if tamano_actual + tamano > max_units and lote_actual:
            lotes.append(lote_actual)
            lote_actual = [texto]
            tamano_actual = tamano
        else:
            lote_actual.append(texto)
            tamano_actual += tamano

    if lote_actual:
        lotes.append(lote_actual)

    desglose = []
    translator = GoogleTranslator(source="en", target="es")

    for i, batch in enumerate(lotes, 1):
        unidades = sum(len(s) for s in batch)
        desglose.append(
            {"lote_num": i, "elementos": len(batch), "unidades": unidades}
        )

    return jsonify({
        "total_citas": len(df_citas),
        "total_peticiones": len(lotes),
        "total_caracteres": int(df_citas["cita_en"].str.len().sum()),
        "desglose": desglose,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)