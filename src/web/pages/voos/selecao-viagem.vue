
<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <h1 class="text-2xl font-bold text-grayScale-900">Seleção de Voos</h1>

    <!-- Card Ida -->
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-6">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h2 class="text-lg font-bold flex items-center gap-2">
            <img src="/images/plane-takeoff.svg" class="w-6 h-6" />
            Voo de Ida
          </h2>
          <p class="text-sm text-grayScale-600 mt-1 capitalize">
            {{ storeVoos.selectionParams.origin_city }} para {{ storeVoos.selectionParams.destination_city }}
          </p>
          <p class="text-sm text-grayScale-600">
            {{ formatarData(storeVoos.selectionParams.departure_date) }}
          </p>
        </div>
        <button 
          @click="selecionarIda"
          class="text-primary hover:text-primary-dark font-medium text-sm"
        >
          {{ storeVoos.outboundFlight ? 'Alterar voo' : 'Selecionar voo' }}
        </button>
      </div>

      <!-- Voo Selecionado -->
      <div v-if="storeVoos.outboundFlight" class="bg-white border rounded-lg p-4">
        <div class="flex justify-between items-center">
            <div class="flex gap-4 items-center">
                <div>
                    <p class="font-bold">{{ storeVoos.outboundFlight.airline_name }}</p>
                    <p class="text-sm text-grayScale-600">Voo {{ storeVoos.outboundFlight.flight_number }}</p>
                </div>
            </div>
            <div class="text-right">
                <p class="font-bold">{{ formatarHora(storeVoos.outboundFlight.departure_time) }} - {{ formatarHora(storeVoos.outboundFlight.estimated_arrival) }}</p>
                <p class="text-sm text-grayScale-600">{{ calcularDuracao(storeVoos.outboundFlight.departure_time, storeVoos.outboundFlight.estimated_arrival) }}</p>
            </div>
        </div>
      </div>
      <div v-else class="bg-grayScale-100 border border-dashed border-grayScale-300 rounded-lg p-8 text-center text-grayScale-500">
        Nenhum voo selecionado
      </div>
    </div>

    <!-- Card Volta -->
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-6">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h2 class="text-lg font-bold flex items-center gap-2">
            <img src="/images/plane-takeoff.svg" class="w-6 h-6 transform scale-x-[-1]" />
            Voo de Volta
          </h2>
          <p class="text-sm text-grayScale-600 mt-1 capitalize">
            {{ storeVoos.selectionParams.destination_city }} para {{ storeVoos.selectionParams.origin_city }}
          </p>
          <p class="text-sm text-grayScale-600">
            {{ formatarData(storeVoos.selectionParams.return_date) }}
          </p>
        </div>
        <button 
          @click="selecionarVolta"
          class="text-primary hover:text-primary-dark font-medium text-sm"
        >
          {{ storeVoos.inboundFlight ? 'Alterar voo' : 'Selecionar voo' }}
        </button>
      </div>

      <!-- Voo Selecionado -->
      <div v-if="storeVoos.inboundFlight" class="bg-white border rounded-lg p-4">
         <div class="flex justify-between items-center">
            <div class="flex gap-4 items-center">
                <div>
                    <p class="font-bold">{{ storeVoos.inboundFlight.airline_name }}</p>
                    <p class="text-sm text-grayScale-600">Voo {{ storeVoos.inboundFlight.flight_number }}</p>
                </div>
            </div>
            <div class="text-right">
                <p class="font-bold">{{ formatarHora(storeVoos.inboundFlight.departure_time) }} - {{ formatarHora(storeVoos.inboundFlight.estimated_arrival) }}</p>
                <p class="text-sm text-grayScale-600">{{ calcularDuracao(storeVoos.inboundFlight.departure_time, storeVoos.inboundFlight.estimated_arrival) }}</p>
            </div>
        </div>
      </div>
      <div v-else class="bg-grayScale-100 border border-dashed border-grayScale-300 rounded-lg p-8 text-center text-grayScale-500">
        Nenhum voo selecionado
      </div>
    </div>

    <!-- Botão Continuar -->
    <div class="flex justify-end">
      <button 
        :disabled="!podeContinuar"
        @click="continuar"
        class="bg-primary hover:bg-primary-dark disabled:bg-grayScale-400 text-white w-full md:w-auto px-8 py-3 rounded-lg font-semibold transition-colors shadow-lg"
      >
        Continuar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';

definePageMeta({
  middleware: ["rota-autenticada"],
});

const router = useRouter();
const storeVoos = useStoreVoos();

// Redirect to home if no params (page refresh without state)
if (!storeVoos.selectionParams.origin_city) {
    router.push('/');
}

const podeContinuar = computed(() => {
  return storeVoos.outboundFlight && storeVoos.inboundFlight;
});



function formatarHora(datetime: string) {
  return new Date(datetime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function formatarData(datetime: string) {
    if (!datetime) return '';
  return new Date(datetime).toLocaleDateString('pt-BR');
}

function calcularDuracao(saida: string, chegada: string) {
  const diff = new Date(chegada).getTime() - new Date(saida).getTime();
  const horas = Math.floor(diff / (1000 * 60 * 60));
  const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${horas}h ${minutos}min`;
}

function selecionarIda() {
  router.push({
    path: '/voos',
    query: {
      origin_city: storeVoos.selectionParams.origin_city,
      destination_city: storeVoos.selectionParams.destination_city,
      departure_date: storeVoos.selectionParams.departure_date,
      selectionMode: 'outbound'
    }
  });
}

function selecionarVolta() {
  router.push({
    path: '/voos',
    query: {
      origin_city: storeVoos.selectionParams.destination_city, // Invertido
      destination_city: storeVoos.selectionParams.origin_city, // Invertido
      departure_date: storeVoos.selectionParams.return_date, // Data da volta
      selectionMode: 'inbound'
    }
  });
}

function continuar() {
    if (podeContinuar.value) {
        router.push('/checkout/passageiros');
    }
}
</script>
