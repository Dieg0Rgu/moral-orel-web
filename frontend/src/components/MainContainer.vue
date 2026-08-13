<script setup>
import { ref } from 'vue'

// Control de pestaña activa (1, 2 o 3)
const tabActiva = ref(2) // Ponemos 2 (Polemista) por defecto o 1 según prefieras

// --- PESTAÑA 1: BUSCADOR DE VIBRAS ---
const situacion = ref('')
const resultadosVibras = ref([])
const cargandoVibras = ref(false)

const buscarVibras = async () => {
  if (situacion.value.length < 10) return
  cargandoVibras.value = true
  try {
    const res = await fetch('/api/vibras', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ situacion: situacion.value })
    })
    const data = await res.json()
    resultadosVibras.value = data.resultados || []
  } catch (e) {
    console.error(e)
  } finally {
    cargandoVibras.value = false
  }
}

// --- PESTAÑA 2: EL POLEMISTA DEVOTO (6 Párrafos) ---
const pregunta = ref('')
const ensayoResultado = ref(null)
const cargandoPolemista = ref(false)

const generarEnsayo = async () => {
  if (!pregunta.value.trim()) return
  cargandoPolemista.value = true
  try {
    const res = await fetch('/api/polemista', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta: pregunta.value })
    })
    const data = await res.json()
    ensayoResultado.value = data
  } catch (e) {
    console.error(e)
  } finally {
    cargandoPolemista.value = false
  }
}

// --- PESTAÑA 3: EMPAQUETADOR DE CITAS ---
const maxUnits = ref(200)
const empaquetado = ref(null)
const cargandoEmpaquetador = ref(false)

const procesarLotes = async () => {
  cargandoEmpaquetador.value = true
  try {
    const res = await fetch('/api/empaquetador', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ max_units: maxUnits.value })
    })
    empaquetado.value = await res.json()
  } catch (e) {
    console.error(e)
  } finally {
    cargandoEmpaquetador.value = false
  }
}
</script>

<template>
  <div class="panel-container">
    <!-- BARRA DE PESTAÑAS NATIVAS DE TU INTERFAZ -->
    <nav class="tabs-header">
      <button 
        :class="['tab-btn', { active: tabActiva === 1 }]" 
        @click="tabActiva = 1">
        1. BUSCADOR DE VIBRAS
      </button>
      <button 
        :class="['tab-btn', { active: tabActiva === 2 }]" 
        @click="tabActiva = 2">
        2. EL POLEMISTA DEVOTO
      </button>
      <button 
        :class="['tab-btn', { active: tabActiva === 3 }]" 
        @click="tabActiva = 3">
        3. EMPAQUETADOR DE CITAS
      </button>
    </nav>

    <div class="tab-content">
      <!-- ------------------- PESTAÑA 1 ------------------- -->
      <section v-if="tabActiva === 1">
        <h2>Buscador Semántico de Culpas y Vibras</h2>
        <p class="description">Confiesa tu situación o estado emocional para encontrar el proverbio adecuado:</p>

        <textarea 
          v-model="situacion" 
          placeholder="Ej: Cometí un error en el trabajo y me da miedo confesar la verdad..."
          rows="5"
        ></textarea>

        <button class="action-btn" @click="buscarVibras" :disabled="cargandoVibras">
          {{ cargandoVibras ? 'INSPECTANDO ALMA...' : 'BUSCAR CONSUELO SEMÁNTICO' }}
        </button>

        <!-- Resultados Vibras -->
        <div v-if="resultadosVibras.length" class="results-box">
          <div v-for="(res, i) in resultadosVibras" :key="i" class="card-quote">
            <p class="quote">"{{ res.cita_es }}"</p>
            <span class="author">— {{ res.autor }} (Afinidad: {{ res.afinidad }})</span>
          </div>
        </div>
      </section>

      <!-- ------------------- PESTAÑA 2 ------------------- -->
      <section v-if="tabActiva === 2">
        <h2>El Polemista Devoto</h2>
        <p class="description">Ingresa un dilema moral o pregunta teológica para recibir un sermón académico de 6 párrafos:</p>

        <textarea 
          v-model="pregunta" 
          placeholder="Ej: ¿Es moralmente justificable mentir para proteger a un inocente?"
          rows="4"
        ></textarea>

        <button class="action-btn" @click="generarEnsayo" :disabled="cargandoPolemista">
          {{ cargandoPolemista ? 'REDACTANDO SERMÓN...' : 'GENERAR DEBATE MORAL' }}
        </button>

        <!-- Resultado Ensayo de 6 Párrafos -->
        <article v-if="ensayoResultado" class="sermon-article">
          <h3>{{ ensayoResultado.titulo }}</h3>

          <div class="paragraph-block">
            <span class="p-tag">Exordio (Introducción)</span>
            <p>{{ ensayoResultado.intro }}</p>
          </div>

          <div class="paragraph-block">
            <span class="p-tag">Dogma y Argumentación (Desarrollo)</span>
            <p v-for="(parrafo, idx) in ensayoResultado.desarrollo" :key="idx">
              {{ parrafo }}
            </p>
          </div>

          <div class="paragraph-block">
            <span class="p-tag">Sentencia Final (Conclusión)</span>
            <p>{{ ensayoResultado.conclusion }}</p>
          </div>

          <div class="quote-footer" v-if="ensayoResultado.autor">
            <small>Cita Canónica Aplicada: <em>"{{ ensayoResultado.cita_original }}"</em> — <strong>{{ ensayoResultado.autor }}</strong></small>
          </div>
        </article>
      </section>

      <!-- ------------------- PESTAÑA 3 ------------------- -->
      <section v-if="tabActiva === 3">
        <h2>Empaquetador de Citas y Presupuesto</h2>
        <p class="description">Calcula el fraccionamiento de peticiones según el límite de caracteres por lote:</p>

        <div class="input-inline">
          <label>Unidades Máximas por Lote:</label>
          <input type="number" v-model="maxUnits" />
        </div>

        <button class="action-btn" @click="procesarLotes" :disabled="cargandoEmpaquetador">
          {{ cargandoEmpaquetador ? 'CALCULANDO...' : 'EMPAQUETAR CITAS' }}
        </button>

        <div v-if="empaquetado" class="results-box">
          <p><strong>Total Citas:</strong> {{ empaquetado.total_citas }} | <strong>Peticiones Necesarias:</strong> {{ empaquetado.total_peticiones }}</p>
          <ul class="batch-list">
            <li v-for="lote in empaquetado.desglose" :key="lote.lote_num">
              Lote {{ lote.lote_num }}: {{ lote.elementos }} elementos ({{ lote.unidades }} caracteres)
            </li>
          </ul>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.panel-container {
  max-width: 900px;
  margin: 2rem auto;
  border: 1px solid #800000;
  box-shadow: 0 0 20px rgba(128, 0, 0, 0.4);
  background-color: #121212;
  border-radius: 4px;
}

.tabs-header {
  display: flex;
  background-color: #050505;
  border-bottom: 1px solid #800000;
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: transparent;
  color: #ccc;
  border: none;
  border-right: 1px solid #333;
  font-family: 'Georgia', serif;
  font-size: 0.85rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:last-child {
  border-right: none;
}

.tab-btn.active {
  background-color: #990000;
  color: #ffffff;
}

.tab-content {
  padding: 2rem;
  color: #e0e0e0;
}

h2 {
  font-family: 'Cinzel', 'Georgia', serif;
  color: #ffffff;
  margin-top: 0;
}

.description {
  color: #aaa;
  margin-bottom: 1.5rem;
}

textarea, input[type="number"] {
  width: 100%;
  background-color: #000;
  border: 1px solid #800000;
  color: #fff;
  padding: 12px;
  font-family: inherit;
  box-sizing: border-box;
  margin-bottom: 1.5rem;
}

textarea:focus, input:focus {
  outline: none;
  border-color: #ffcc00;
}

.action-btn {
  width: 100%;
  background: linear-gradient(to bottom, #990000, #660000);
  border: 1px solid #ffcc00;
  color: #ffcc00;
  padding: 14px;
  font-family: 'Cinzel', 'Georgia', serif;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  letter-spacing: 1px;
}

.action-btn:hover:not(:disabled) {
  background: #b30000;
}

.sermon-article {
  margin-top: 2rem;
  border-top: 1px solid #444;
  padding-top: 1.5rem;
}

.paragraph-block {
  margin-bottom: 1.5rem;
  background: #0a0a0a;
  padding: 1rem;
  border-left: 3px solid #990000;
}

.p-tag {
  color: #ffcc00;
  font-size: 0.75rem;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.5rem;
}

.quote-footer {
  background-color: #1a0000;
  border: 1px solid #800000;
  padding: 1rem;
  color: #ffcc00;
  margin-top: 1rem;
}
</style>