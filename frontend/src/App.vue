<script setup>
import Header from './components/Header.vue'
import MainContainer from './components/MainContainer.vue'
</script>

<template>
  <div class="app-layout">
    <Header />
    <MainContainer />
  </div>
</template>

<style>
/* Estilos globales */
body {
  margin: 0;
  background-color: #ffffff;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

.app-layout {
  padding: 2rem 1rem;
  min-height: 100vh;
}
</style>