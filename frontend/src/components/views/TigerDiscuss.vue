<script setup>
import { ref } from 'vue'

const pregunta = ref('')
const cargando = ref(false)
const error = ref(null)
const resultado = ref(null)

const generarEnsayo = async () => {
  if (!pregunta.value.trim()) return
  cargando.value = true
  error.value = null

  try {
    const res = await fetch('/api/polemista', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta: pregunta.value })
    })
    const data = await res.json()
    if (!res.ok || data.error) throw new Error(data.error || 'Error al generar')
    resultado.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
}
</script>

<template>

  
  <div class="tab-content">
    <form @submit.prevent="generarEnsayo" class="input-group">
      <input type="text" v-model="pregunta" placeholder="Tema o dilema moral..." :disabled="cargando" required />
      <button type="submit" :disabled="cargando">{{ cargando ? 'Generando...' : 'Generar Ensayo' }}</button>
    </form>

    <div v-if="cargando" class="status loading">Sintetizando ensayo académico de 6 párrafos...</div>
    <div v-if="error" class="status error">{{ error }}</div>

    <article v-if="resultado && !cargando" class="essay">
      <h2>{{ resultado.titulo }}</h2>
      <div class="card intro"><span class="badge">Introducción</span><p>{{ resultado.intro }}</p></div>
      <div class="card desarrollo">
        <span class="badge">Desarrollo</span>
        <p v-for="(p, i) in resultado.desarrollo" :key="i">{{ p }}</p>
      </div>
      <div class="card conclusion"><span class="badge">Conclusión</span><p>{{ resultado.conclusion }}</p></div>
      <footer v-if="resultado.autor" class="quote-card">
        📖 Cita: "{{ resultado.cita_original }}" — <strong>{{ resultado.autor }}</strong>
      </footer>
    </article>
  </div>
</template>

<style scoped>
/* Asegurar que las entradas de texto se vean claras */
input, textarea {
  width: 100%;
  padding: 12px;
  background-color: #0f172a;
  border: 1px solid #475569;
  border-radius: 8px;
  color: #ffffff;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #38bdf8;
}

button {
  padding: 12px 20px;
  background-color: #0284c7;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #0369a1;
}

/* Tarjetas de resultados o párrafos */
.card, .quote-card, .vibra-card {
  background-color: #0f172a;
  border: 1px solid #334155;
  border-left: 4px solid #38bdf8;
  color: #e2e8f0;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 6px;
}
</style>