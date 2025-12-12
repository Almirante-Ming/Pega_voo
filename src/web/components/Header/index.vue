<template>
  <header class="header w-full relative">
    <div class="w-full h-[64px] bg-primary flex items-center justify-between px-5 font-bold text-white relative">
      
      <!-- Menu Button -->
      <button v-if="showMenu" @click="$emit('toggleSidebar')" class="p-1 hover:bg-white/10 rounded">
        <Icon name-icon="Bars3Icon" class="size-6 text-white" />
      </button>

      <!-- Theme Toggle (Only when Menu is hidden - Auth pages) -->
      <button v-else @click="toggleTheme" class="p-1 hover:bg-white/10 rounded transition-colors" title="Alternar Tema">
          <Icon :name-icon="currentTheme === 'dark' ? 'MoonIcon' : 'SunIcon'" class="size-6 text-white" />
      </button>

      <!-- Centered Logo -->
      <div class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <NuxtLink to="/">
          <img src="@/assets/images/logo.png" alt="Logo" class="h-14 w-auto object-contain cursor-pointer" />
        </NuxtLink>
      </div>

    </div>
  </header>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";
import { useRoute } from 'vue-router';
import { computed, ref, onMounted } from 'vue';

defineEmits<{
  (e: "toggleSidebar"): void;
}>();

const route = useRoute();
const currentTheme = ref('light');

const showMenu = computed(() => {
  const hiddenRoutes = ['/login', '/cadastro', '/recuperarSenha'];
  return !hiddenRoutes.includes(route.path);
});

onMounted(() => {
    // Check system or saved preference
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        currentTheme.value = 'dark';
        document.documentElement.classList.add('dark');
    } else {
        currentTheme.value = 'light';
        document.documentElement.classList.remove('dark');
    }
});

function toggleTheme() {
    if (currentTheme.value === 'dark') {
        currentTheme.value = 'light';
        localStorage.theme = 'light';
        document.documentElement.classList.remove('dark');
    } else {
        currentTheme.value = 'dark';
        localStorage.theme = 'dark';
        document.documentElement.classList.add('dark');
    }
}
</script>

<style scoped>
</style>