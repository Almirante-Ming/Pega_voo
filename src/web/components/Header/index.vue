<template>
  <header class="header">
    <div class="w-full h-20 bg-primary flex items-center justify-between px-5 font-bold text-success">
      <div class="text-grayScale-100">
        Meu voo
      </div>
      
      <button 
        @click="toggleTheme"
        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-grayScale-200 hover:bg-grayScale-300 dark:bg-grayScale-700 dark:hover:bg-grayScale-600 transition-colors duration-200 text-grayScale-800 dark:text-grayScale-200"
        :title="isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'"
      >
        <span class="text-lg">{{ isDark ? '☀️' : '🌙' }}</span>
        <span class="text-sm font-medium">{{ isDark ? 'Claro' : 'Escuro' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
  const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
</style>