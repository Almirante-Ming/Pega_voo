<template>
  <div>
    <!-- Backdrop -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-gray-950/50 backdrop-blur-sm z-40 transition-opacity transition-colors duration-300"
      @click="$emit('close')"
    ></div>

    <!-- Sidebar -->
    <aside
      class="fixed top-0 left-0 h-full w-[80%] max-w-[500px] bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-4 border-b border-grayScale-200 flex items-center justify-between text-grayScale-700">
        <span class="text-xl font-bold">Menu</span>
        <button @click="$emit('close')" class="p-1 hover:bg-white/10 rounded">
          <Icon name-icon="XMarkIcon" class="size-6 text-grayScale-700" />
        </button>
      </div>

      <nav class="flex-1 p-4 overflow-y-auto">
        <ul class="space-y-2">
          <li>
            <NuxtLink
              to="/voos"
              class="flex items-center gap-3 px-4 py-3 text-grayScale-700 rounded-lg hover:bg-primary-50 hover:text-primary transition-colors duration-200"
              @click="$emit('close')"
            >
              <Icon name-icon="PaperAirplaneIcon" class="size-5" />
              <span class="font-medium">Voos</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink
              to="/cadastro"
              class="flex items-center gap-3 px-4 py-3 text-grayScale-700 rounded-lg hover:bg-primary-50 hover:text-primary transition-colors duration-200"
              @click="$emit('close')"
            >
              <Icon name-icon="UserPlusIcon" class="size-5" />
              <span class="font-medium">Cadastro</span>
            </NuxtLink>
          </li>
          <!-- Add more links here based on the pages directory if needed -->
        </ul>
      </nav>
    </aside>
  </div>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";

defineProps<{
  isOpen: boolean;
}>();

defineEmits<{
  (e: "close"): void;
}>();
</script>

<style scoped></style>
