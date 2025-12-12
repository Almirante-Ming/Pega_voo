<template>
  <div>
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm z-[90] transition-opacity duration-300"
      @click="$emit('close')"
    ></div>

    <aside
      class="fixed top-0 left-0 h-full w-[85%] max-w-[320px] bg-grayScale-50 shadow-2xl z-[100] transform transition-transform duration-300 ease-out flex flex-col"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
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
            class="first:bg-grayScale-50"
          />
        </ul>
      </nav>

      <div class="p-6 border-t border-grayScale-100 bg-grayScale-50 relative">
        <div 
          v-if="showSettings" 
          class="absolute bottom-20 left-4 right-4 bg-grayScale-200 rounded-xl shadow-xl border border-grayScale-100 overflow-hidden transform transition-all duration-200 origin-bottom"
        >
             <div class="p-2 flex flex-col gap-1">
                 <!-- Theme Toggle -->
                 <button 
                   @click="toggleTheme"
                   class="flex items-center justify-between w-full px-4 py-3 text-grayScale-700 md:hover:bg-grayScale-50 rounded-lg transition-colors text-sm font-medium"
                 >
                    <div class="flex items-center gap-3">
                        <Icon :name-icon="currentTheme === 'dark' ? 'MoonIcon' : 'SunIcon'" class="size-5 text-grayScale-500" />
                        <span>Tema {{ currentTheme === 'dark' ? 'Escuro' : 'Claro' }}</span>
                    </div>
                 </button>
                 
                 <div class="h-px bg-grayScale-400 my-1"></div>

                 <!-- Logout -->
                 <button 
                   @click="logout"
                   class="flex items-center gap-3 w-full px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors text-sm font-medium"
                 >
                    <Icon name-icon="ArrowLeftOnRectangleIcon" class="size-5" />
                    <span>Sair da conta</span>
                 </button>
             </div>
        </div>

        <button
          @click="showSettings = !showSettings"
          class="flex items-center gap-3 w-full px-4 py-3 text-grayScale-700 rounded-xl hover:bg-grayScale-200 transition-colors duration-200 font-medium"
          :class="{'bg-grayScale-200': showSettings}"
        >
          <Icon name-icon="Cog6ToothIcon" class="size-6 text-grayScale-500" />
          <span>Configurações</span>
          <Icon name-icon="ChevronUpIcon" class="size-4 ml-auto text-grayScale-400" />
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
const showSettings = ref(false);
const currentTheme = ref('light'); // default

const menuItems = [
    { label: 'Início', icon: 'HomeIcon', route: '/' },
    { label: 'Meus Voos', icon: 'TicketIcon', route: '/meus-voos' }
];

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


import { useStoreDeUsuario } from "@/store/useStoreUsuario";

function logout() {
  const store = useStoreDeUsuario();
  store.clearToken();
  emit("close");
  router.push("/login"); 
}

</script>

<style scoped></style>
