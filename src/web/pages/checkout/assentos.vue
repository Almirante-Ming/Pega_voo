<template>
  <div class="min-h-screen bg-grayScale-50 pb-32 md:pb-10 relative">
    <div class="max-w-7xl mx-auto px-1 py-3.5">
      <div class="flex items-center gap-2 mb-4">
        <BackButton />
        <h2 class="text-xl font-bold text-grayScale-900">Mapa de assentos</h2>
      </div>
      
      <div class="flex flex-col lg:flex-row gap-8">
        <div class="flex-1 flex flex-col gap-6">
            <!-- Flight Toggle (if Round Trip) -->
            <div v-if="store.inboundFlight" class="flex gap-4 px-2">
                <div class="flex-1">
                    <span class="text-sm font-normal">Ida:</span>

                    <button 
                    @click="currentFlight = 'outbound'"
                    class="w-full py-3 px-4 rounded-lg font-bold border-2 relative transition-colors flex justify-between items-center"
                    :class="currentFlight === 'outbound' ? 'border-primary bg-primary/5 text-primary' : 'border-grayScale-200 bg-white text-grayScale-600'"
                    >
                    <div class="flex flex-col gap-1 text-center">
                        <div class="flex flex-col items-center leading-none gap-0.5">
                            <span>{{ store.outboundFlight?.origin_city }}</span>
                            <Icon nameIcon="ArrowDownIcon" class="w-3 h-3 text-grayScale-400" />
                            <span>{{ store.outboundFlight?.destination_city }}</span>
                        </div>
                                            <span v-if="store.selectedSeats[store.outboundFlight?.id]" class="text-xs text-green-500 font-medium">Assento escolhido</span>

                    </div>
                    </button>
                </div>

                <div class="flex-1">
                    <span class="text-sm font-normal">Volta:</span>

                    <button 
                    @click="currentFlight = 'inbound'"
                    class="w-full py-3 px-4 rounded-lg font-bold border-2 relative transition-colors flex justify-between items-center"
                    :class="currentFlight === 'inbound' ? 'border-primary bg-primary/5 text-primary' : 'border-grayScale-200 bg-white text-grayScale-600'"
                    >
                    <div class="flex flex-col gap-1 text-center">
                        <div class="flex flex-col items-center leading-none gap-0.5">
                            <span>{{ store.inboundFlight?.origin_city }}</span>
                            <Icon nameIcon="ArrowDownIcon" class="w-3 h-3 text-grayScale-400" />
                            <span>{{ store.inboundFlight?.destination_city }}</span>
                        </div>
                                            <span v-if="store.selectedSeats[store.inboundFlight?.id]" class="text-xs text-green-500 font-medium">Assento escolhido</span>

                    </div>
                    </button>
                </div>
            </div>
            
             <!-- Seat Map Card -->
            <div class="bg-white rounded-lg shadow-sm border border-grayScale-200 p-3.5 pb-0 flex flex-col items-center">
                <div class="w-full flex justify-between items-center">
                    <div class="gap-4 text-xs text-grayScale-600 w-full grid grid-cols-2 border p-4 rounded-md">
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-grayScale-100 border border-grayScale-300 rounded"></div> Disponível</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-primary rounded"></div> Selecionado</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 bg-grayScale-200 rounded opacity-50"></div> Ocupado</div>
                        <div class="flex items-center gap-1"><div class="w-4 h-4 border-2 border-primary rounded flex items-center justify-center"><Icon nameIcon="StarIcon" class="w-3 h-3 text-primary" /></div> Premium</div>
                    </div>
                </div>

                <!-- Aircraft Body -->
                <div class="bg-grayScale-50 rounded-full rounded-t-[100px] pb-2 relative min-w-[300px]">
                    <!-- Cockpit area visual decoration -->
                    <div class="absolute top-8 left-1/2 transform -translate-x-1/2 text-grayScale-300">
                        <img src="@/assets/images/plane-icon.png" class="w-8 h-8 opacity-50" />
                    </div>

                    <div class="mt-12 flex flex-col gap-3">
                        <div class="flex justify-between w-full px-8 mb-2 font-bold text-grayScale-400">
                            <span>A</span><span>B</span><span>C</span>
                            <span class="w-8"></span>
                            <span>D</span><span>E</span><span>F</span>
                        </div>

                        <!-- Rows -->
                        <div v-for="row in rows" :key="row.number" class="flex items-center gap-4">
                            <!-- Left Side -->
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
                                    <Icon v-if="getSeatData(row.number, seat)?.seat_class === 'premium'" nameIcon="StarIcon" class="w-3 h-3 absolute -top-1 -right-1 text-yellow-500 bg-white rounded-full" />
                                </button>
                            </div>
                            
                            <!-- Aisle -->
                            <div class="w-8 text-center text-xs text-grayScale-300">{{ row.number }}</div>

                            <!-- Right Side -->
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
                                    <Icon v-if="getSeatData(row.number, seat)?.seat_class === 'premium'" nameIcon="StarIcon" class="w-3 h-3 absolute -top-1 -right-1 text-yellow-500 bg-white rounded-full" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Desktop Summary (Side) -->
        <div class="hidden lg:block w-80">
            <div class="bg-white rounded-lg shadow-lg p-6 sticky top-6">
                <h3 class="font-bold text-lg mb-4">Resumo da Compra</h3>
                <div class="flex flex-col gap-3 text-sm text-grayScale-600 border-b border-grayScale-200 pb-4 mb-4">
                    <div class="flex justify-between">
                        <span>Voo de Ida</span>
                        <span>R$ {{ store.outboundFlight?.tickets?.[store.ticketClass] }}</span>
                    </div>
                    <div v-if="store.inboundFlight" class="flex justify-between">
                        <span>Voo de Volta</span>
                        <span>R$ {{ store.inboundFlight?.tickets?.[store.ticketClass] }}</span>
                    </div>
                     <div class="flex justify-between" v-if="store.outboundFlight">
                         <span class="text-xs">
                            Assento Ida ({{ store.selectedSeats[store.outboundFlight.id] || '-' }})
                        </span>
                     </div>
                     <div class="flex justify-between" v-if="store.inboundFlight">
                         <span class="text-xs">
                             Assento Volta ({{ store.selectedSeats[store.inboundFlight.id] || '-' }})
                         </span>
                     </div>
                </div>
                <div class="flex justify-between items-center mb-6">
                    <span class="font-bold text-grayScale-900">Total</span>
                    <span class="font-bold text-2xl text-primary">R$ {{ store.totalPrice }}</span>
                </div>
                <button 
                    @click="finalizar"
                    :disabled="!isSelectionComplete"
                    class="w-full bg-primary hover:bg-primary-dark disabled:bg-grayScale-400 text-white py-3 rounded-lg font-bold transition-colors"
                >
                    Finalizar Compra
                </button>
            </div>
        </div>
      </div>
    </div>

    <!-- Mobile Summary (Fixed Bottom) -->
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-grayScale-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] p-4 z-50">
        <div class="flex flex-col gap-2">
             <div 
               @click="mobileDetailsOpen = !mobileDetailsOpen"
               class="flex justify-between items-center cursor-pointer"
             >
                <div class="flex items-center gap-2">
                    <span class="font-bold text-grayScale-900">Total</span>
                    <Icon :nameIcon="mobileDetailsOpen ? 'ChevronDownIcon' : 'ChevronUpIcon'" class="w-4 h-4 text-grayScale-500" />
                </div>
                <span class="font-bold text-xl text-primary">R$ {{ store.totalPrice }}</span>
             </div>
             
             <div v-if="mobileDetailsOpen" class="text-sm text-grayScale-600 py-2 border-b border-grayScale-100 mb-2">
                 <div class="flex justify-between">
                     <span>Voo de Ida</span>
                     <span>R$ {{ store.outboundFlight?.tickets?.[store.ticketClass] }}</span>
                 </div>
                 <div v-if="store.inboundFlight" class="flex justify-between mt-1">
                     <span>Voo de Volta</span>
                     <span>R$ {{ store.inboundFlight?.tickets?.[store.ticketClass] }}</span>
                 </div>
                 <div class="flex justify-between mt-1">
                     <span>Assentos:</span>
                     <span>
                         {{ store.selectedSeats[store.outboundFlight?.id] || '-' }} / 
                         {{ store.selectedSeats[store.inboundFlight?.id] || '-' }}
                     </span>
                 </div>
             </div>

             <button 
                @click="finalizar"
                :disabled="!isSelectionComplete"
                class="w-full bg-primary hover:bg-primary-dark disabled:bg-grayScale-400 text-white py-3 rounded-lg font-bold transition-colors"
            >
                Finalizar Compra
            </button>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';
import { useApi } from '@/composables/useApi';

definePageMeta({
  middleware: ["rota-autenticada"],
});

const store = useStoreVoos();
const router = useRouter();
const mobileDetailsOpen = ref(false);
const currentFlight = ref<'outbound' | 'inbound'>('outbound');
const { execute, data, error, loading } = useApi('get', '', {});

// flightNumber -> Seat[]
const seatsData = ref<Record<string, any[]>>({}); 

async function fetchSeats(flight: any) {
    if (!flight) return;
    try {
        // Create a separate instance/call for each flight to avoid race conditions with specific `execute`
        // Actually useApi is designed for one endpoint. I should probably re-use execute but update URL.
        // Or cleaner: make a small helper or just fetch sequentially.
        const { execute: fetchExec, data: fetchData } = useApi('get', `/flights/seats/by-number/${flight.flight_number}`, {});
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

// Move to next flight automatically if Outbound is done
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
    
    // Find max row
    let maxRow = 0;
    seats.forEach(s => {
        const match = s.seat_number.match(/(\d+)([A-Z])/);
        if (match) {
            const r = parseInt(match[1]);
            if (r > maxRow) maxRow = r;
        }
    });

    // Determine premium based on current data (assuming premium seats have class 'premium' or similar)
    // Or we can just build the rows and let the seat object dictate the class.
    
    // Generate valid rows 1..maxRow
    const result = [];
    for (let i = 1; i <= maxRow; i++) {
        // Check if any seat in this row is premium to mark the row layout? 
        // Not strictly necessary for layout, but visual help.
        // We'll pass the whole row number and find seats in template.
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
    if (!s) return true; // Seat doesn't exist (e.g. gap in map)
    
    // 1. Availability
    if (!s.is_available) return true;

    // 2. Class Constraint
    // store.ticketClass is 'economy' or 'premium'
    // seat.seat_class is 'economy' or 'premium' (API)
    if (store.ticketClass !== s.seat_class) return true;
    
    return false;
}

function getSeatClass(row: number, seat: string) {
    const s = getSeatData(row, seat);
    if (!s) return 'invisible'; // Hide non-existent seats

    if (isSeatSelected(row, seat)) {
        return 'bg-primary text-white border-primary';
    }
    
    const isPremium = s.seat_class === 'premium';

    if (isSeatDisabled(row, seat)) {
         return 'bg-grayScale-100 text-grayScale-300 cursor-not-allowed';
    }
    
    if (isPremium) {
        return 'bg-white border-2 border-purple-500 text-purple-700 hover:bg-purple-50';
    }
    return 'bg-white border border-grayScale-300 text-grayScale-600 hover:border-primary hover:text-primary';
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
    alert('Compra realizada com sucesso!');
    router.push('/meus-voos');
}
</script>
