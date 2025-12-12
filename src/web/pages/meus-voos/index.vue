<template>
  <div class="min-h-screen bg-grayScale-50 pb-20">
    <div class="max-w-4xl mx-auto p-4">
      <!-- Header -->
      <div class="flex items-center gap-2 mb-6">
        <BackButton />
        <h1 class="text-2xl font-bold text-grayScale-900">Meus Voos</h1>
      </div>

      <!-- Tabs -->
      <div class="flex border-b border-grayScale-200 mb-6">
          <button 
            @click="activeTab = 'upcoming'"
            class="px-6 py-2 font-medium transition-colors border-b-2"
            :class="activeTab === 'upcoming' ? 'border-primary text-primary' : 'border-transparent text-grayScale-500 hover:text-grayScale-700'"
          >
              Próximos
          </button>
          <button 
            @click="activeTab = 'history'"
            class="px-6 py-2 font-medium transition-colors border-b-2"
            :class="activeTab === 'history' ? 'border-primary text-primary' : 'border-transparent text-grayScale-500 hover:text-grayScale-700'"
          >
              Histórico
          </button>
      </div>

      <!-- Content -->
      <div v-if="loading" class="flex justify-center p-8">
          <Icon nameIcon="ArrowPathIcon" class="w-8 h-8 text-primary animate-spin" />
      </div>

      <div v-else-if="currentList.length === 0" class="text-center py-12 bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-200">
          <Icon nameIcon="TicketIcon" class="w-12 h-12 text-grayScale-300 mx-auto mb-3" />
          <h3 class="text-lg font-bold text-grayScale-900 mb-1">Nenhum voo encontrado</h3>
          <p class="text-grayScale-500">Você não tem voos nesta categoria.</p>
      </div>

      <div v-else class="flex flex-col gap-4">
          <div v-for="ticket in currentList" :key="ticket.ticket_id" class="bg-grayScale-50 rounded-xl shadow-md border-l-4 overflow-hidden hover:shadow-lg transition-shadow duration-300"
            :class="{
                'border-green-500': ticket.status === 'confirmed' || ticket.status === 'reserved',
                'border-red-500': ticket.status === 'cancelled',
                'border-yellow-500': ticket.status === 'pending' || ticket.status === 'marked'
            }"
          >
              <div class="p-5">
                <!-- Header: Airline & Status -->
                <div class="flex justify-between items-center mb-4">
                     <div class="flex items-center gap-3">
                        <div class="bg-grayScale-100 p-1 rounded-lg w-10">
                            <img src="/assets/images/plane-icon.png" />
                        </div>
                        <div>
                            <p class="font-bold text-grayScale-900 leading-tight">
                                {{ ticket.flight?.airline_name || 'Companhia Aérea' }}
                            </p>
                            <p class="text-xs text-grayScale-500">Voo {{ ticket.flight?.flight_number || ticket.flight_id }}</p>
                        </div>
                     </div>
                     
                     <div class="px-3 py-1 text-xs font-bold uppercase rounded-full"
                        :class="{
                            'bg-green-100 text-green-700': ticket.status === 'confirmed' || ticket.status === 'reserved',
                            'bg-red-100 text-red-700': ticket.status === 'cancelled',
                            'bg-yellow-100 text-yellow-700': ticket.status === 'pending' || ticket.status === 'marked'
                        }"
                     >
                        {{ formatStatus(ticket.status) }}
                     </div>
                </div>

                <div class="flex items-center justify-between mb-5">
                    <div class="text-center min-w-[80px]">
                        <p class="text-lg font-black text-grayScale-900">{{ ticket.flight?.origin_airport || '---' }}</p>
                        <p class="text-xs text-grayScale-500 font-medium">{{ ticket.flight?.origin_city || 'Origem' }}</p>
                        <p class="text-sm font-semibold text-grayScale-700 mt-1">
                            {{ ticket.flight ? formatTime(ticket.flight.departure_time) : formatTime(ticket.boarding_time) }}
                        </p>
                    </div>

                    <div class="flex-1 px-4 flex flex-col items-center">
                        <div class="w-full flex items-center justify-center gap-2">
                             <div class="h-[2px] w-full bg-grayScale-200"></div>
                             <Icon nameIcon="PaperAirplaneIcon" class="w-4 h-4 text-grayScale-300 rotate-90" />
                             <div class="h-[2px] w-full bg-grayScale-200"></div>
                        </div>
                         <p class="text-xs text-grayScale-400 mt-1 text-center">
                             {{ formatDate(ticket.boarding_time) }}
                         </p>
                    </div>

                    <div class="text-center min-w-[80px]">
                        <p class="text-lg font-black text-grayScale-900">{{ ticket.flight?.destination_airport || '---' }}</p>
                        <p class="text-xs text-grayScale-500 font-medium">{{ ticket.flight?.destination_city || 'Destino' }}</p>
                         <p class="text-sm font-semibold text-grayScale-700 mt-1">
                             {{ ticket.flight ? formatTime(ticket.flight.estimated_arrival) : '--:--' }}
                        </p>
                    </div>
                </div>

                <div class="flex justify-between items-center pt-4 border-t border-grayScale-100">
                    <div class="flex gap-4">
                         <div>
                             <span class="block text-[10px] text-grayScale-400 uppercase font-bold tracking-wider">Classe</span>
                             <span class="text-sm font-semibold text-grayScale-800">
                                 {{ ticket.seat_class === 'premium' ? 'Premium' : 'Econômica' }}
                             </span>
                         </div>
                    </div>
                    <div>
                        <span class="block text-[10px] text-right text-grayScale-400 uppercase font-bold tracking-wider">Preço</span>
                        <span class="text-lg font-bold text-primary">R$ {{ ticket.price }}</span>
                    </div>
                </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useApi } from '@/composables/useApi';
import BackButton from '@/components/BackButton/index.vue';
import Icon from '@/components/Icon/index.vue';

definePageMeta({
  middleware: ["rota-autenticada"],
});

const activeTab = ref<'upcoming' | 'history'>('upcoming');
const tickets = ref<any[]>([]);

// Busca as passagens do usuário
const { execute, loading, data, error } = useApi('get', '/tickets/my-tickets', {});

const { $axios } = useNuxtApp();
onMounted(async () => {
    await execute();
    if (data.value) {
        // Normaliza a resposta da API
        const rawTickets = Array.isArray(data.value) ? data.value : (data.value.items || []);
        
        // Busca detalhes dos voos associados
        const flightIds = [...new Set(rawTickets.map((t: any) => t.flight_id))];
        const flightDetails = new Map();

        await Promise.all(flightIds.map(async (fid) => {
            try {
                const res = await $axios.get(`/flights/${fid}`);
                if(res.data) flightDetails.set(fid, res.data);
            } catch (e) {
                console.error(`Falha ao buscar voo ${fid}`, e);
            }
        }));

        tickets.value = rawTickets.map((t: any) => {
             return {
                 ...t,
                 flight: flightDetails.get(t.flight_id) || null
             }
        });
    }
});

const currentList = computed(() => {
    const now = new Date();
    return tickets.value.filter(t => {
        const dateStr = t.boarding_time;
        if (!dateStr) return false;
        
        const dep = new Date(dateStr);
        
        if (activeTab.value === 'upcoming') {
            return dep >= now;
        } else {
            return dep < now;
        }
    }).sort((a, b) => {
        const da = new Date(a.boarding_time).getTime();
        const db = new Date(b.boarding_time).getTime();
        return activeTab.value === 'upcoming' ? da - db : db - da; 
    });
});

function formatDate(str: string) {
    if(!str) return '';
    return new Date(str).toLocaleDateString('pt-BR', { 
        day: '2-digit', month: 'long', year: 'numeric'
    });
}

function formatTime(str: string) {
    if(!str) return '--:--';
    return new Date(str).toLocaleTimeString('pt-BR', {
        hour: '2-digit', minute: '2-digit'
    });
}

function formatStatus(status: string) {
    const map: Record<string, string> = {
        'reserved': 'Confirmado',
        'confirmed': 'Confirmado',
        'cancelled': 'Cancelado',
        'pending': 'Pendente',
        'marked': 'Marcado'
    };
    return map[status] || status;
}
</script>
