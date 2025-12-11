<template>
  <div class="min-h-screen bg-grayScale-100 flex flex-col items-center justify-center p-4">
    <div class="w-full max-w-md bg-grayScale-50 rounded-lg shadow-xl overflow-hidden">
      <!-- Header -->
      <div class="bg-blue-900 p-4 flex justify-between items-center text-grayScale-50">
          <span class="font-bold text-lg">Cancelamento</span>
          <div class="font-bold text-xl italic">PEGA VOO</div>
      </div>
      
      <!-- Red Cancel Banner -->
      <div class="bg-red-500 p-8 text-center text-grayScale-50 flex flex-col items-center gap-4">
          <div class="w-20 h-20 rounded-full border-4 border-grayScale-50 flex items-center justify-center">
              <Icon nameIcon="XMarkIcon" class="w-10 h-10 text-grayScale-50" />
          </div>
          <div>
              <h1 class="text-2xl font-bold mb-2">Reserva cancelada</h1>
              <p class="text-red-50">O pagamento não foi processado.</p>
          </div>
      </div>

      <!-- Content -->
      <div class="p-6 flex flex-col gap-6 text-center">
          <p class="text-grayScale-600">
              Você cancelou a operação ou ocorreu um erro durante o pagamento. 
              Nenhuma cobrança foi efetuada.
          </p>

          <!-- Actions -->
          <div class="flex flex-col gap-3 mt-4">
              <button @click="router.push('/voos')" class="w-full bg-blue-900 hover:bg-blue-800 text-grayScale-50 py-3 rounded-lg font-bold transition-colors">
                  Tentar novamente
              </button>
              <button @click="router.push('/')" class="w-full bg-grayScale-50 border border-grayScale-300 hover:bg-grayScale-50 text-grayScale-900 py-3 rounded-lg font-bold transition-colors">
                  Voltar à tela inicial
              </button>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';
import Icon from '@/components/Icon/index.vue';

const store = useStoreVoos();
const router = useRouter();

onMounted(() => {
    // Clear selection on cancel too, forcing clean restart
    store.clearSelection();
});
</script>
