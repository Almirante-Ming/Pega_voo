<template>
  <div class="flex flex-col items-center justify-center drop-shadow-md">
    <div class="w-full max-w-md rounded-lg overflow-hidden">
      <!-- Cabeçalho -->

      
      <!-- Banner Verde de Sucesso -->
      <div class="bg-green-500 p-6 text-center text-white flex flex-col items-center gap-4">
          <div class="w-20 h-20 rounded-full border-4 border-white flex items-center justify-center">
              <Icon nameIcon="CheckIcon" class="w-10 h-10 text-white" />
          </div>
          <div>
              <h1 class="text-2xl font-bold mb-2">Reserva confirmada!</h1>
              <p class="text-green-50">Sua viagem está garantida.</p>
          </div>
      </div>

      <!-- Detalhes do Bilhete -->
      <div class="p-6 flex flex-col gap-6 bg-grayScale-50">
          <div v-if="localFlight" class="flex flex-col gap-4">
              <!-- Rota -->
              <div class="flex items-start gap-4">
                  <Icon nameIcon="PaperAirplaneIcon" class="w-6 h-6 text-grayScale-500 mt-1" />
                  <div>
                      <span class="block text-xs text-grayScale-500">Origem - Destino</span>
                      <span class="font-bold text-grayScale-900">{{ localFlight.origin_city }} para {{ localFlight.destination_city }}</span>
                  </div>
              </div>

               <!-- Partida -->
               <div class="flex items-start gap-4">
                  <Icon nameIcon="CalendarIcon" class="w-6 h-6 text-grayScale-500 mt-1" />
                  <div>
                      <span class="block text-xs text-grayScale-500">Data e Hora de Partida</span>
                      <span class="font-bold text-grayScale-900">{{ formatDate(localFlight.departure_time) }}</span>
                  </div>
              </div>

               <!-- Chegada (Mockado ou calculado se disponível, geralmente hora de chegada está no obj voo) -->
               <!-- Usando Hora de Partida + Duração por enquanto ou apenas genérico se não estiver no obj mock -->
               
               <!-- Número do Voo -->
               <div class="flex items-start gap-4">
                  <Icon nameIcon="TicketIcon" class="w-6 h-6 text-grayScale-500 mt-1" />
                  <div>
                      <span class="block text-xs text-grayScale-500">Número do Voo</span>
                      <span class="font-bold text-grayScale-900">Voo {{ localFlight.flight_number }} ({{ localFlight.airline_name }})</span>
                  </div>
              </div>
          </div>
          <div v-else class="text-center text-grayScale-500">
              Detalhes da reserva não disponíveis.
          </div>

          <!-- Ações -->
          <div class="flex flex-col gap-3 mt-4">
              <button @click="router.push('/meus-voos')" class="w-full bg-blue-900 hover:bg-blue-800 text-white py-3 rounded-lg font-semibold transition-colors">
                  Ver reserva
              </button>
              <button @click="router.push('/')" class="w-full bg-grayScale-200 border border-grayScale-300 hover:bg-grayScale-50 text-grayScale-900 py-3 rounded-lg font-semibold transition-colors">
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

// Cópia local dos dados do voo antes de limpar a store
const localFlight = ref<any>(null);

onMounted(() => {
    // Preferir dados da store se disponíveis (ex: se não limpamos ainda ou navegação SPA preservou, embora improvável com redirecionamento externo)
    if (store.outboundFlight) {
        localFlight.value = { ...store.outboundFlight };
    } else {
        // Fallback para dados persistidos no localStorage
        const cached = localStorage.getItem('last_payment_flight');
        if (cached) {
            try {
                localFlight.value = JSON.parse(cached);
            } catch (e) {
                console.error("Failed to parse cached flight details", e);
            }
            // Limpar cache para não persistir para sempre
            localStorage.removeItem('last_payment_flight');
        }
    }
    
    // Limpar a store para prevenir voltar ou estado obsoleto
    store.clearSelection();
});

function formatDate(str: string) {
    if(!str) return '';
    return new Date(str).toLocaleDateString('pt-BR', { 
         day: '2-digit', month: 'long', year: 'numeric',
         hour: '2-digit', minute: '2-digit'
    });
}
</script>
