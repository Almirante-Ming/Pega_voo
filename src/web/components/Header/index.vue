<template>
  <header class="header w-full relative">
    <div class="w-full h-[64px] bg-primary flex items-center justify-between px-5 font-bold text-grayScale-50 relative">
      
      <!-- Menu Button -->
      <button v-if="showMenu" @click="$emit('toggleSidebar')" class="p-1 hover:bg-grayScale-200 rounded">
        <Icon name-icon="Bars3Icon" class="size-6 text-grayScale-50" />
      </button>

      <!-- Centered Logo -->
      <div class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <img src="@/assets/images/logo.png" alt="Logo" class="h-14 w-auto object-contain" />
      </div>

    </div>
  </header>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";

defineEmits<{
  (e: "toggleSidebar"): void;
}>();

const route = useRoute();
const showMenu = computed(() => {
  const hiddenRoutes = ['/login', '/cadastro', '/recuperarSenha'];
  return !hiddenRoutes.includes(route.path);
});
</script>

<style scoped>
</style>