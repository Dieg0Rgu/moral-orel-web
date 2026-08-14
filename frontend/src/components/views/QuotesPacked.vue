<template>
  <div class="quotes-packed-container">
    <h2>📦 Empaquetador de Citas por Lotes</h2>
    <p class="subtitle">
      Ajusta el límite de unidades para calcular la distribución óptima de
      peticiones.
    </p>

    <!-- Formulario de control -->
    <div class="controls-card">
      <div class="input-group">
        <label for="limit">Unidades máximas por lote:</label>
        <input
          id="limit"
          v-model.number="limiteUnidades"
          type="number"
          step="50"
          min="50"
          placeholder="Ej. 200"
        />
      </div>
      <button @click="calcularLotes" class="btn-primary">Calcular Lotes</button>
    </div>

    <!-- Resultados -->
    <div v-if="resultado" class="results-section">
      <!-- Tarjetas de Métricas -->
      <div class="metrics-grid">
        <div class="metric-card">
          <span class="metric-label">Total Citas</span>
          <span class="metric-value">{{ resultado.total_citas }}</span>
        </div>
        <div class="metric-card highlight">
          <span class="metric-label">Peticiones API</span>
          <span class="metric-value">{{ resultado.total_peticiones }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Total Caracteres</span>
          <span class="metric-value">{{
            resultado.total_caracteres.toLocaleString()
          }}</span>
        </div>
      </div>

      <!-- Tabla Estructurada -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Lote #</th>
              <th># Citas</th>
              <th>Unidades / Caracteres</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lote in resultado.desglose" :key="lote.lote_num">
              <td class="badge-cell">
                <span class="batch-badge"> Lote {{ lote.lote_num }} </span>
              </td>

              <td>{{ lote.elementos }}</td>

              <td class="units-cell">
                {{ lote.unidades }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const limiteUnidades = ref(200);
const resultado = ref(null);
// 1. Estado de carga
const cargando = ref(false);

const calcularLotes = async () => {
  cargando.value = true;

  try {
    const res = await fetch("/api/empaquetador", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        limite: limiteUnidades.value,
      }),
    });

    const data = await res.json();

    console.log("Respuesta completa:", JSON.stringify(data, null, 2));
    console.log("Propiedades:", Object.keys(data));

    resultado.value = data;
  } catch (error) {
    console.error("Error al calcular lotes:", error);
  } finally {
    cargando.value = false;
  }
};
</script>

<style scoped>
/* Estilo opcional para opacar el botón mientras está deshabilitado */
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quotes-packed-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h2 {
  font-size: 1.5rem;
  color: #f8fafc;
}

.subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-top: -0.5rem;
}

/* Formulario */
.controls-card {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  background-color: #0f172a;
  padding: 1.25rem;
  border-radius: 8px;
  border: 1px solid #334155;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.input-group label {
  font-size: 0.875rem;
  color: #cbd5e1;
  font-weight: 500;
}

.btn-primary {
  background-color: #0284c7;
  color: #ffffff;
  font-weight: 600;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #0369a1;
}

/* Grilla de Métricas / KPIs */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background-color: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-card.highlight {
  border-color: #38bdf8;
  background-color: rgba(56, 189, 248, 0.05);
}

.metric-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8fafc;
}

.metric-card.highlight .metric-value {
  color: #38bdf8;
}

/* Tabla de Datos */
.table-container {
  border: 1px solid #334155;
  border-radius: 8px;
  overflow: hidden;
  max-height: 400px;
  overflow-y: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.95rem;
}

.data-table th {
  background-color: #0f172a;
  color: #cbd5e1;
  padding: 0.85rem 1rem;
  font-weight: 600;
  border-bottom: 1px solid #334155;
  position: sticky;
  top: 0;
}

.data-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #1e293b;
  color: #e2e8f0;
}

.data-table tbody tr:hover {
  background-color: rgba(56, 189, 248, 0.03);
}

.batch-badge {
  background-color: #1e293b;
  border: 1px solid #475569;
  color: #38bdf8;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.units-cell {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  color: #f1f5f9;
}
</style>
