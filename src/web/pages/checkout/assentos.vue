<template>
  <div class="min-h-screen pb-32 md:pb-10 relative">
    <div class="max-w-7xl mx-auto px-1 py-3.5">
      <div class="flex items-center gap-2 mb-4 px-3">
        <BackButton />
        <h2 class="text-xl font-bold text-grayScale-900">Mapa de assentos</h2>
      </div>
      
      <div class="flex flex-col lg:flex-row gap-8">
        <div class="flex-1 flex flex-col gap-4">
            <!-- Alternar voo (se for Ida e Volta) -->
            <div v-if="store.inboundFlight" class="flex gap-4">
                <div class="flex-1">
                    <div class="bg-primary w-fit text-grayScale-50 px-2 rounded-lg pb-0.5 mb-1">
                        <span class="text-sm font-medium">Ida</span>
                    </div>

                    <button 
                    @click="currentFlight = 'outbound'"
                    class="w-full py-3 px-4 rounded-lg font-bold border-2 relative transition-colors flex justify-center items-center"
                    :class="currentFlight === 'outbound' ? 'border-primary bg-primary/5 text-primary' : 'border-grayScale-300 bg-grayScale-50 text-grayScale-600'"
                    >
                    <div class="flex flex-col gap-1 text-center">
                        <div class="flex flex-col items-center leading-none gap-0.5">
                            <span>{{ store.outboundFlight?.origin_city }}</span>
                            <Icon nameIcon="ArrowDownIcon" class="w-3 h-3 text-grayScale-400" />
                            <span>{{ store.outboundFlight?.destination_city }}</span>
                        </div>
                    </div>
                    <div v-if="store.selectedSeats[store.outboundFlight?.id]" 
                         class="absolute -bottom-3 -right-3 w-8 h-8 rounded-full bg-green-600 text-grayScale-50 flex items-center justify-center text-xs font-bold shadow-sm border-2 border-grayScale-50">
                        {{ store.selectedSeats[store.outboundFlight?.id] }}
                    </div>
                    </button>
                </div>

                <div class="flex-1">
                    <div class="bg-primary w-fit text-grayScale-50 px-2 rounded-lg pb-0.5 mb-1">
                        <span class="text-sm font-medium">Volta</span>
                    </div>
                    <button 
                    @click="currentFlight = 'inbound'"
                    class="w-full py-3 px-4 rounded-lg font-bold border-2 relative transition-colors flex justify-center items-center"
                    :class="currentFlight === 'inbound' ? 'border-primary bg-primary/5 text-primary' : 'border-grayScale-300 bg-grayScale-50 text-grayScale-600'"
                    >
                    <div class="flex flex-col gap-1 text-center">
                        <div class="flex flex-col items-center leading-none gap-0.5">
                            <span>{{ store.inboundFlight?.origin_city }}</span>
                            <Icon nameIcon="ArrowDownIcon" class="w-3 h-3 text-grayScale-400" />
                            <span>{{ store.inboundFlight?.destination_city }}</span>
                        </div>
                    </div>
                    <div v-if="store.selectedSeats[store.inboundFlight?.id]" 
                         class="absolute -bottom-3 -right-3 w-8 h-8 rounded-full bg-green-600 text-grayScale-50 flex items-center justify-center text-xs font-bold shadow-sm border-2 border-grayScale-50">
                        {{ store.selectedSeats[store.inboundFlight?.id] }}
                    </div>
                    </button>
                </div>
            </div>
            
             <!-- Cartão do Mapa de Assentos -->
            <div class="bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-300 p-3.5 pb-0 flex flex-col items-center">
                <div class="w-full flex justify-between items-center">
                    <div class="gap-4 text-xs text-grayScale-600 w-full grid grid-cols-2 border p-4 rounded-md">
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-grayScale-100 border border-grayScale-300 rounded"></div> Disponível</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-primary rounded"></div> Selecionado</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-grayScale-200 rounded opacity-50"></div> Ocupado</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 border-2 border-primary rounded flex items-center justify-center"><Icon nameIcon="StarIcon" class="w-3 h-3 text-primary" /></div> Premium</div>
                    </div>
                </div>

                <!-- Corpo da Aeronave -->
                <div class="bg-grayScale-50 rounded-full rounded-t-[100px] pb-2 relative min-w-[300px]">
                    <!-- Decoração visual da área da cabine -->
                    <div class="absolute top-8 left-1/2 transform -translate-x-1/2 text-grayScale-300">
                        <img src="@/assets/images/plane-icon.png" class="w-8 h-8 opacity-50" />
                    </div>

                    <div class="mt-12 flex flex-col gap-3">
                        <div class="flex justify-between w-full px-8 mb-2 font-bold text-grayScale-400">
                            <span>A</span><span>B</span><span>C</span>
                            <span class="w-8"></span>
                            <span>D</span><span>E</span><span>F</span>
                        </div>

                        <!-- Fileiras -->
                        <div v-for="row in rows" :key="row.number" class="flex items-center gap-4">
                            <!-- Lado Esquerdo -->
                            <div class="flex gap-2">
                                <button 
                                  v-for="seat in ['A', 'B', 'C']"
                                  :key="seat"
                                  @click="selectSeat(row.number, seat)"
                                  :disabled="isSeatDisabled(row.number, seat)"
                                  class="w-8 h-10 rounded text-xs font-bold flex items-center justify-center transition-all relative"
                                  :class="getSeatClass(row.number, seat)"
                                >
                                    {{ seat }}
                                    <Icon v-if="getSeatData(row.number, seat)?.seat_class === 'premium'" nameIcon="StarIcon" class="w-3 h-3 absolute -top-1 -right-1 text-yellow-500 bg-grayScale-50 rounded-full" />
                                </button>
                            </div>
                            
                            <!-- Corredor -->
                            <div class="w-8 text-center text-xs text-grayScale-500">{{ row.number }}</div>

                            <!-- Lado Direito -->
                            <div class="flex gap-2">
                                <button 
                                  v-for="seat in ['D', 'E', 'F']"
                                  :key="seat"
                                  @click="selectSeat(row.number, seat)"
                                  :disabled="isSeatDisabled(row.number, seat)"
                                  class="w-8 h-10 rounded text-xs font-bold flex items-center justify-center transition-all relative"
                                  :class="getSeatClass(row.number, seat)"
                                >
                                    {{ seat }}
                                    <Icon v-if="getSeatData(row.number, seat)?.seat_class === 'premium'" nameIcon="StarIcon" class="w-3 h-3 absolute -top-1 -right-1 text-yellow-500 bg-grayScale-50 rounded-full" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Componente de Resumo -->
        <CheckoutSummary 
            buttonText="Finalizar Compra" 
            :showSeats="true"
            :disabled="!isSelectionComplete"
            @submit="finalizar" 
        />
      </div>
    </div>
  </div>
</template>
 
 <script setup lang="ts">
 import { useStoreVoos } from '@/store/useStoreVoos';
 import { useApi } from '@/composables/useApi';
import CheckoutSummary from '@/components/CheckoutSummary/index.vue';
 
 definePageMeta({
   middleware: ["rota-autenticada"],
 });
 
 const store = useStoreVoos();
 const router = useRouter();
 
 const currentFlight = ref<'outbound' | 'inbound'>('outbound');
 const { execute, data, error, loading } = useApi('get', '', {});
 
 const seatsData = ref<Record<string, any[]>>({}); 
 
 const requiredClass = computed(() => {
    return currentFlight.value === 'outbound' ? store.outboundTicketClass : store.inboundTicketClass;
 });
 
 async function fetchSeats(flight: any) {
     if (!flight) return;
     try {
         // Busca assentos do voo
         const { execute: fetchExec, data: fetchData } = useApi('get', `/flights/${flight.id}/seats`, {});
         await fetchExec();
         if (fetchData.value) {
             seatsData.value[flight.flight_number] = fetchData.value;
         }
     } catch (e) {
         console.error('Error fetching seats', e);
     }
 }
 
 onMounted(async () => {
     if (store.outboundFlight) {
         await fetchSeats(store.outboundFlight);
     }
     if (store.inboundFlight) {
         await fetchSeats(store.inboundFlight);
     }
 });
 
 // Mover para o próximo voo automaticamente se a Ida estiver pronta
 watch(() => store.selectedSeats[store.outboundFlight?.id], (newVal) => {
     if (newVal && store.inboundFlight && !store.selectedSeats[store.inboundFlight.id]) {
         setTimeout(() => {
             currentFlight.value = 'inbound';
         }, 500);
     }
 });
 
 function getActiveFlight() {
     return currentFlight.value === 'outbound' ? store.outboundFlight : store.inboundFlight;
 }
 
 const currentSeats = computed(() => {
     const flight = getActiveFlight();
     if (!flight) return [];
     return seatsData.value[flight.flight_number] || [];
 });
 
 const rows = computed(() => {
     const seats = currentSeats.value;
     if (seats.length === 0) return [];
     
     // Encontrar maior fileira
     let maxRow = 0;
     seats.forEach(s => {
         const match = s.seat_number.match(/(\d+)([A-Z])/);
         if (match) {
             const r = parseInt(match[1]);
             if (r > maxRow) maxRow = r;
         }
     });
 

     // Gerar fileiras válidas 1..maxRow
     const result = [];
     for (let i = 1; i <= maxRow; i++) {
         result.push({ number: i });
     }
     return result;
 });
 
 function getSeatData(row: number, col: string) {
     const seatCode = `${row}${col}`;
     return currentSeats.value.find(s => s.seat_number === seatCode);
 }
 
 function isSeatSelected(row: number, seat: string) {
     const flight = getActiveFlight();
     if (!flight) return false;
     return store.selectedSeats[flight.id] === `${row}${seat}`;
 }
 
 function isSeatDisabled(row: number, seat: string) {
     const s = getSeatData(row, seat);
     if (!s) return true;
     
     // 1. Disponibilidade
     if (!s.is_available) return true;
 
     // 2. Restrição de Classe
     if (requiredClass.value !== s.seat_class) return true;
     
     return false;
 }

function getSeatClass(row: number, seat: string) {
    const s = getSeatData(row, seat);
    if (!s) return 'invisible';

    if (isSeatSelected(row, seat)) {
        return 'bg-primary text-grayScale-50 border-primary';
    }
    
    const isPremium = s.seat_class === 'premium';

    if (isSeatDisabled(row, seat)) {
         return 'bg-grayScale-100 text-grayScale-300 cursor-not-allowed';
    }
    
    if (isPremium) {
        return 'bg-grayScale-50 border-2 border-purple-500 text-purple-700 hover:bg-purple-50';
    }
    return 'bg-grayScale-50 border border-grayScale-300 text-grayScale-600 hover:border-primary hover:text-primary';
}

function selectSeat(row: number, seat: string) {
    const flight = getActiveFlight();
    if (flight) {
        store.selectSeat(flight.id, `${row}${seat}`);
    }
}

const isSelectionComplete = computed(() => {
    const outboundOk = !!store.selectedSeats[store.outboundFlight?.id];
    const inboundOk = !store.inboundFlight || !!store.selectedSeats[store.inboundFlight.id];
    return outboundOk && inboundOk;
});

function finalizar() {
    router.push('/checkout/resumo');
}
</script>
