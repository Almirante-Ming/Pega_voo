<template>
  <header class="header">
    <div class="w-full h-20 bg-primary flex items-center justify-between px-5 font-bold text-success">
      <div>
        Meu voo
      </div>
      
      <button 
        @click="toggleTheme"
        class="flex items-center gap-2 px-3 py-2 rounded-lg bg-grayScale-800 hover:bg-grayScale-900 transition-colors duration-200"
        :title="isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'"
      >
        <span class="text-lg">{{ isDark ? '☀️' : '🌙' }}</span>
        <span class="text-sm font-medium">{{ isDark ? 'Claro' : 'Escuro' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
</script>

<style scoped>
</style>