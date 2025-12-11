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

      <div v-else-if="currentList.length === 0" class="text-center py-12 bg-white rounded-lg shadow-sm border border-grayScale-200">
          <Icon nameIcon="TicketIcon" class="w-12 h-12 text-grayScale-300 mx-auto mb-3" />
          <h3 class="text-lg font-bold text-grayScale-900 mb-1">Nenhum voo encontrado</h3>
          <p class="text-grayScale-500">Você não tem voos nesta categoria.</p>
      </div>

      <div v-else class="flex flex-col gap-4">
          <div v-for="ticket in currentList" :key="ticket.ticket_id" class="bg-white rounded-lg p-5 shadow-sm border border-grayScale-200 relative overflow-hidden">
              <!-- Status Badge -->
              <div class="absolute top-0 right-0 px-3 py-1 text-xs font-bold uppercase rounded-bl-lg"
                 :class="{
                     'bg-green-100 text-green-700': ticket.status === 'confirmed' || ticket.status === 'reserved',
                     'bg-red-100 text-red-700': ticket.status === 'cancelled',
                     'bg-yellow-100 text-yellow-700': ticket.status === 'pending'
                 }"
              >
                  {{ formatStatus(ticket.status) }}
              </div>

              <!-- Flight Info -->
              <div v-if="ticket.flight">
                  <div class="flex flex-col gap-2 mb-4">
                      <div class="flex items-center gap-2 font-bold text-lg text-grayScale-900">
                          <span>{{ ticket.flight.origin_city }}</span>
                          <Icon nameIcon="ArrowRightIcon" class="w-5 text-grayScale-400" />
                          <span>{{ ticket.flight.destination_city }}</span>
                      </div>
                      <div class="text-sm text-grayScale-500">
                          {{ formatDate(ticket.flight.departure_time) }}
                      </div>
                  </div>

                  <!-- Details Card -->
                  <div class="bg-grayScale-50 p-4 rounded-lg border border-grayScale-100 flex flex-col md:flex-row gap-4 md:items-center justify-between">
                      <div class="flex items-center gap-3">
                           <div class="bg-white p-2 rounded-full border border-grayScale-200">
                               <Icon nameIcon="PaperAirplaneIcon" class="w-5 h-5 -rotate-45 text-primary" />
                           </div>
                           <div>
                               <p class="font-bold text-grayScale-900">{{ ticket.flight.airline_name }} <span class="text-grayScale-400 font-normal text-xs">(Voo {{ ticket.flight.flight_number }})</span></p>
                               <p class="text-xs text-grayScale-500">Classe {{ ticket.seat_class === 'premium' ? 'Premium' : 'Econômica' }}</p>
                           </div>
                      </div>
                      
                      <div class="flex gap-6 items-center border-t md:border-t-0 border-grayScale-200 pt-3 md:pt-0">
                          <div>
                              <span class="block text-xs text-grayScale-400 uppercase font-bold">Assento</span>
                              <span class="font-bold text-grayScale-900 text-lg">{{ ticket.seat_number }}</span>
                          </div>
                           <div>
                              <span class="block text-xs text-grayScale-400 uppercase font-bold">Valor</span>
                              <span class="font-bold text-grayScale-900">R$ {{ ticket.price }}</span>
                          </div>
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

// Assuming endpoint returns array of tickets
const { execute, loading, data, error } = useApi('get', '/tickets/my-tickets', {});

onMounted(async () => {
    await execute();
    if (data.value) {
        // Handle if data is wrapped or direct array
        tickets.value = Array.isArray(data.value) ? data.value : (data.value.items || []);
    }
});

const currentList = computed(() => {
    const now = new Date();
    return tickets.value.filter(t => {
        if (!t.flight) return false;
        const dep = new Date(t.flight.departure_time);
        
        if (activeTab.value === 'upcoming') {
            return dep >= now;
        } else {
            return dep < now;
        }
    }).sort((a, b) => {
        const da = new Date(a.flight.departure_time).getTime();
        const db = new Date(b.flight.departure_time).getTime();
        return activeTab.value === 'upcoming' ? da - db : db - da; // Ascending for upcoming, Descending for history
    });
});

function formatDate(str: string) {
    if(!str) return '';
    return new Date(str).toLocaleDateString('pt-BR', { 
        day: '2-digit', month: 'long', year: 'numeric', 
        hour: '2-digit', minute: '2-digit' 
    });
}

function formatStatus(status: string) {
    const map: Record<string, string> = {
        'reserved': 'Confirmado',
        'confirmed': 'Confirmado',
        'cancelled': 'Cancelado',
        'pending': 'Pendente'
    };
    return map[status] || status;
}
</script>
