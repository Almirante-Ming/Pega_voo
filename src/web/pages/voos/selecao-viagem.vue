
<template>
  <div class="max-w-7xl mx-auto pb-32 lg:pb-10">
    <div class="flex items-center gap-2 mb-6">
        <BackButton />
        <h1 class="text-2xl font-bold text-grayScale-900">Seleção de Voos</h1>
    </div>

    <div class="flex flex-col lg:flex-row gap-8">
        <!-- Coluna Esquerda: Cartões de Voo -->
        <div class="flex-1 space-y-6">
            <!-- Card Ida -->
            <div class="bg-grayScale-50 rounded-lg shadow-lg p-6">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <h2 class="text-lg font-bold flex items-center gap-2 text-grayScale-900">
                    <img src="/images/plane-takeoff.svg" class="w-6 h-6 dark:bg-grayScale-800 dark:p-1 rounded-full" />
                    Voo de Ida
                  </h2>
                  <p class="text-sm text-grayScale-600 mt-1 capitalize">
                    {{ storeVoos.outboundFlight ? storeVoos.outboundFlight.origin_city : storeVoos.selectionParams.origin_city }} para {{ storeVoos.outboundFlight ? storeVoos.outboundFlight.destination_city : storeVoos.selectionParams.destination_city }}
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
              <div v-if="storeVoos.outboundFlight" class="bg-grayScale-50 border rounded-lg p-4">
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
                  <h2 class="text-lg font-bold flex items-center gap-2 text-grayScale-900">
                    <img src="/images/plane-takeoff.svg" class="w-6 h-6 transform scale-x-[-1] dark:bg-grayScale-800 dark:p-1 rounded-full" />
                    Voo de Volta
                  </h2>
                  <p class="text-sm text-grayScale-600 mt-1 capitalize">
                    {{ storeVoos.inboundFlight ? storeVoos.inboundFlight.origin_city : storeVoos.selectionParams.destination_city }} para {{ storeVoos.inboundFlight ? storeVoos.inboundFlight.destination_city : storeVoos.selectionParams.origin_city }}
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
              <div v-if="storeVoos.inboundFlight" class="bg-grayScale-50 border rounded-lg p-4">
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
        </div>

        <!-- Coluna Direita: Resumo (Desktop) -->
        <div class="hidden lg:block w-80">
            <div class="bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-300 p-6 sticky top-24">
                <h3 class="font-bold text-lg mb-4">Resumo da Viagem</h3>
                
                <div class="flex flex-col gap-3 text-sm text-grayScale-600 border-b border-grayScale-300 pb-4 mb-4">
                    <div class="flex justify-between" v-if="storeVoos.outboundFlight">
                        <span>Voo de Ida</span>
                        <span>R$ {{ storeVoos.outboundFlight.tickets?.economy }}</span>
                    </div>
                    <div v-if="storeVoos.inboundFlight" class="flex justify-between">
                        <span>Voo de Volta</span>
                        <span>R$ {{ storeVoos.inboundFlight.tickets?.economy }}</span>
                    </div>
                    <div v-if="!storeVoos.outboundFlight && !storeVoos.inboundFlight" class="text-grayScale-400 italic">
                        Selecione os voos para ver o resumo
                    </div>
                </div>

                <div class="flex justify-between items-end mb-6">
                    <span class="text-sm text-grayScale-600">Total</span>
                    <div class="text-right">
                        <span class="text-2xl font-bold text-primary">R$ {{ storeVoos.ticketsTotal }}</span>
                    </div>
                </div>

                <button 
                  @click="continuar"
                  :disabled="!podeContinuar"
                  class="w-full bg-primary hover:bg-primary-dark disabled:bg-grayScale-300 disabled:cursor-not-allowed text-grayScale-50 py-3 rounded-lg font-bold transition-colors"
                >
                  Continuar
                </button>
            </div>
        </div>
    </div>

    <!-- Rodapé Fixo Mobile -->
    <div class="lg:hidden fixed bottom-0 left-0 w-full bg-grayScale-50 border-t border-grayScale-300 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-50">
        <div class="p-4">
             <!-- Alternar Detalhes -->
             <div 
               @click="mobileDetailsOpen = !mobileDetailsOpen"
               class="flex justify-center mb-2 cursor-pointer"
             >
                 <Icon :nameIcon="mobileDetailsOpen ? 'ChevronDownIcon' : 'ChevronUpIcon'" class="w-5 h-5 text-grayScale-400" />
             </div>
             
             <!-- Detalhes Colapsáveis -->
             <div v-if="mobileDetailsOpen" class="text-sm text-grayScale-600 py-2 border-b border-grayScale-100 mb-2">
                 <div class="flex justify-between" v-if="storeVoos.outboundFlight">
                     <span>Voo de Ida</span>
                     <span>R$ {{ storeVoos.outboundFlight.tickets?.economy }}</span>
                 </div>
                 <div v-if="storeVoos.inboundFlight" class="flex justify-between mt-1">
                     <span>Voo de Volta</span>
                     <span>R$ {{ storeVoos.inboundFlight.tickets?.economy }}</span>
                 </div>
             </div>

             <div class="flex gap-4 items-center">
                 <div class="flex-1">
                     <p class="text-xs text-grayScale-500">Total</p>
                     <p class="text-xl font-bold text-primary">R$ {{ storeVoos.ticketsTotal }}</p>
                 </div>
                 <button 
                   @click="continuar"
                   :disabled="!podeContinuar"
                   class="bg-primary hover:bg-primary-dark disabled:bg-grayScale-300 disabled:cursor-not-allowed text-grayScale-50 px-6 py-3 rounded-lg font-bold transition-colors"
                 >
                   Continuar
                 </button>
             </div>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';

definePageMeta({
  middleware: ["rota-autenticada"],
});
import BackButton from '@/components/BackButton/index.vue';

const router = useRouter();
const storeVoos = useStoreVoos();
const mobileDetailsOpen = ref(false);

// Redireciona para home se sem parâmetros (atualização de página sem estado)
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
      origin_city: storeVoos.selectionParams.destination_city,
      destination_city: storeVoos.selectionParams.origin_city,
      departure_date: storeVoos.selectionParams.return_date,
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
