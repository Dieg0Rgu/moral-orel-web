<script setup>
import { ref } from 'vue'

// Importaciones con rutas relativas directas a la subcarpeta views/
import Eco from './views/Eco.vue'
import TigerDiscuss from './views/TigerDiscuss.vue'
import QuotesPacked from './views/QuotesPacked.vue'

const ventanaActual = ref('polemista')
</script>

<template>
  <main class="main-container">
    <nav class="tabs-nav">
      <button 
        :class="{ active: ventanaActual === 'polemista' }" 
        @click="ventanaActual = 'polemista'"
      >
        ⚖️ Tiger Discuss
      </button>
      <button 
        :class="{ active: ventanaActual === 'vibras' }" 
        @click="ventanaActual = 'vibras'"
      >
        🔮 Eco
      </button>
      <button 
        :class="{ active: ventanaActual === 'empaquetador' }" 
        @click="ventanaActual = 'empaquetador'"
      >
        📦 Quotes Packed
      </button>
    </nav>

    <div class="view-viewport">
      <TigerDiscuss v-if="ventanaActual === 'polemista'" />
      <Eco v-if="ventanaActual === 'vibras'" />
      <QuotesPacked v-if="ventanaActual === 'empaquetador'" />
    </div>
  </main>
</template>

<style scoped>
.main-container {
  width: 100%;
  margin-top: 1.5rem;
}

/* Navegación por pestañas */
.tabs-nav {
  display: flex;
  gap: 8px;
  border-bottom: 2px solid #334155;
  margin-bottom: -1px; /* Para conectar suavemente con el contenedor */
}

.tabs-nav button {
  padding: 10px 20px;
  background: #0f172a; /* Mismo todo oscuro de la tarjeta */
  border: 1px solid #334155;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  color: #94a3b8;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tabs-nav button:hover {
  color: #f8fafc;
  background: #1e293b;
}

.tabs-nav button.active {
  color: #38bdf8; /* Azul brillante activado */
  background: #111827;
  border-color: #38bdf8 #38bdf8 #111827 #38bdf8;
  font-weight: bold;
}

/* Área donde se cargan las vistas */
.view-viewport {
  background-color: #111827; /* Mismo fondo del contenedor de la imagen */
  border: 1px solid #334155;
  border-radius: 0 10px 10px 10px;
  padding: 2rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  min-height: 400px;
}
</style>