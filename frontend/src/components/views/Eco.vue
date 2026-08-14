<script setup>
import { ref } from 'vue'

const situacion = ref('')
const cargando = ref(false)
const resultados = ref([])

const buscarVibras = async () => {
  if (situacion.value.length < 10) return
  cargando.value = true
  try {
    const res = await fetch('/api/vibras', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ situacion: situacion.value })
    })
    const data = await res.json()
    resultados.value = data.resultados || []
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="tab-content">
    <div class="input-group">
      <input v-model="situacion" placeholder="Describe cómo te sientes o tu situación (mínimo 10 caracteres)..." />
      <button @click="buscarVibras" :disabled="cargando">Buscar Vibras</button>
    </div>

    <div v-if="resultados.length" class="vibras-grid">
      <div v-for="(item, i) in resultados" :key="i" class="vibra-card">
        <span class="match">{{ item.afinidad }} Match</span>
        <p class="es">"{{ item.cita_es }}"</p>
        <p class="en"><em>"{{ item.cita_en }}"</em></p>
        <strong>— {{ item.autor }}</strong>
      </div>
    </div>
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