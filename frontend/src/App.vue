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

<style scoped>
.app-layout {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 1.5rem;
}
</style>