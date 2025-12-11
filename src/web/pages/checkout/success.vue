<template>
  <div class="flex flex-col items-center justify-center drop-shadow-md">
    <div class="w-full max-w-md rounded-lg overflow-hidden">
      <!-- Header -->

      
      <!-- Green Success Banner -->
      <div class="bg-green-500 p-6 text-center text-grayScale-50 flex flex-col items-center gap-4">
          <div class="w-20 h-20 rounded-full border-4 border-grayScale-50 flex items-center justify-center">
              <Icon nameIcon="CheckIcon" class="w-10 h-10 text-grayScale-50" />
          </div>
          <div>
              <h1 class="text-2xl font-bold mb-2">Reserva confirmada!</h1>
              <p class="text-green-50">Sua viagem está garantida.</p>
          </div>
      </div>

      <!-- Ticket Details -->
      <div class="p-6 flex flex-col gap-6 bg-grayScale-50">
          <div v-if="localFlight" class="flex flex-col gap-4">
              <!-- Route -->
              <div class="flex items-start gap-4">
                  <Icon nameIcon="PaperAirplaneIcon" class="w-6 h-6 text-grayScale-500 mt-1" />
                  <div>
                      <span class="block text-xs text-grayScale-500">Origem - Destino</span>
                      <span class="font-bold text-grayScale-900">{{ localFlight.origin_city }} para {{ localFlight.destination_city }}</span>
                  </div>
              </div>

               <!-- Departure -->
               <div class="flex items-start gap-4">
                  <Icon nameIcon="CalendarIcon" class="w-6 h-6 text-grayScale-500 mt-1" />
                  <div>
                      <span class="block text-xs text-grayScale-500">Data e Hora de Partida</span>
                      <span class="font-bold text-grayScale-900">{{ formatDate(localFlight.departure_time) }}</span>
                  </div>
              </div>

               <!-- Arrival (Mocked or calced if available, usually arrival time is in flight obj) -->
               <!-- Using Departure Time + Duration for now or just generic if not in mock obj -->
               
               <!-- Flight Number -->
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

          <!-- Actions -->
          <div class="flex flex-col gap-3 mt-4">
              <button @click="router.push('/voos')" class="w-full bg-blue-900 hover:bg-blue-800 text-grayScale-50 py-3 rounded-lg font-bold transition-colors">
                  Ver reserva
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

// Local copy of flight data before clearing store
const localFlight = ref<any>(null);

onMounted(() => {
    // Prefer store data if available (e.g. if we didn't wipe it yet or SPA navigation preserved it, though unlikely with external redirect)
    if (store.outboundFlight) {
        localFlight.value = { ...store.outboundFlight };
    } else {
        // Fallback to persisted data in localStorage
        const cached = localStorage.getItem('last_payment_flight');
        if (cached) {
            try {
                localFlight.value = JSON.parse(cached);
            } catch (e) {
                console.error("Failed to parse cached flight details", e);
            }
            // Clear cache so it doesn't persist forever
            localStorage.removeItem('last_payment_flight');
        }
    }
    
    // Clear the store to prevent going back or stale state
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
