<template>
  <div>
    <!-- Backdrop with blur -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm z-[90] transition-opacity duration-300"
      @click="$emit('close')"
    ></div>

    <!-- Sidebar -->
    <aside
      class="fixed top-0 left-0 h-full w-[85%] max-w-[320px] bg-grayScale-50 shadow-2xl z-[100] transform transition-transform duration-300 ease-out flex flex-col"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Header with Logo -->
      <div class="p-6 border-b border-grayScale-100 flex items-center justify-between">
        <div class="w-32">
             <img src="@/assets/images/logo.png" alt="Logo" class="w-full h-auto object-contain" />
        </div>
        <button 
          @click="$emit('close')" 
          class="p-2 text-grayScale-500 hover:text-primary hover:bg-primary-50 rounded-full transition-colors"
        >
          <Icon name-icon="XMarkIcon" class="size-6" />
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-6 px-4">
        <ul class="space-y-3">
          <SidebarItem
            v-for="item in menuItems"
            :key="item.route"
            :to="item.route"
            :icon-name="item.icon"
            :label="item.label"
            @on-click="$emit('close')"
          />
        </ul>
      </nav>

      <!-- Footer with Logout -->
      <div class="p-6 border-t border-grayScale-100 bg-grayScale-50">
        <button
          @click="logout"
          class="flex items-center gap-3 w-full px-4 py-3 text-red-600 rounded-xl hover:bg-red-50 transition-colors duration-200 font-medium"
        >
          <Icon name-icon="ArrowLeftOnRectangleIcon" class="size-6" />
          <span>Sair da conta</span>
        </button>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";
import SidebarItem from "./SidebarItem.vue";
import { useRouter } from "vue-router";

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const router = useRouter();

const menuItems = [
    { label: 'Início', icon: 'HomeIcon', route: '/' },
    { label: 'Meus Voos', icon: 'TicketIcon', route: '/meus-voos' },
];

function logout() {
  const token = useCookie("token");
  token.value = null;

  emit("close");
  router.push("/login");
}
</script>

<style scoped></style>
