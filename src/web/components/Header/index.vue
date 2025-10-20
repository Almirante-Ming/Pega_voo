<template>
  <header class="header w-full">
    <div class="w-full h-[60px] bg-primary flex items-center justify-between px-5 font-bold text-white">
      <div>
        Pega voo
      </div>
      
      <button 
        @click="toggleTheme"
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-grayScale-100 hover:bg-grayScale-200 transition-colors duration-200"
        :title="isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'"
      >
        <span class="text-lg">{{ isDark ? '☀️' : '🌙' }}</span>
        <span class="text-sm font-medium text-grayScale-800">{{ isDark ? 'Claro' : 'Escuro' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
const { isDark, toggleTheme } = useTheme();
</script>

<style scoped>
</style>