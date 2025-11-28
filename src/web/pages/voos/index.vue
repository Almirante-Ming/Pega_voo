<template>
  <div class="w-full space-y-4">
    <!-- Header com filtros -->
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">
      <div class="flex items-center justify-between mb-2">
        <h2 class="text-xl font-bold text-grayScale-900">
          {{ voos.length }} {{ voos.length == 0 ? 'Nenhum voo encontrado' : voos.length == 1 ? 'Voo encontrado' : 'Voos encontrados' }} 
        </h2>
        <button 
          @click="router.push('/')"
          class="text-primary hover:text-primary-dark font-medium text-sm bg-grayScale-200 shadow rounded-md p-2 flex items-center gap-2"
        >
          <Icon nameIcon="MagnifyingGlassIcon" class="w-5 h-5" />
          Nova busca
        </button>
      </div>

      <!-- Info da busca -->
      <div class="flex flex-col gap-4 text-sm text-grayScale-700">
        <h2>Resumo da pesquisa</h2>

        <div class="flex gap-2 justify-around text-center">
          <span v-if="filtros.origin_city">
            <strong>Origem:</strong> {{ filtros.origin_city }}
          </span>
          <Icon nameIcon="ArrowRightIcon" class="w-5 h-5 self-center" />
          <span v-if="filtros.destination_city">
            <strong>Destino:</strong> {{ filtros.destination_city }}
          </span>
        </div>

        <span v-if="filtros.departure_date">
          <strong>Data:</strong> {{ formatarData(filtros.departure_date) }}
        </span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Icon nameIcon="ArrowPathIcon" class="w-8 h-8 text-primary animate-spin" />
    </div>

    <!-- Lista de voos -->
    <div v-else-if="voos.length > 0" class="space-y-3">
    <CardVoo
        v-for="voo in voos"
        :key="voo.id"
        :voo="voo"
        :airlineName="getAirlineName(voo.airline_id)"
        :flightNumber="voo.flight_number"
        :departureHour="formatarHora(voo.departure_time)"
        :originAirport="voo.origin_airport"
        :departureDateShort="formatarDataCurta(voo.departure_time)"
        :duration="calcularDuracao(voo.departure_time, voo.estimated_arrival)"
        :arrivalHour="formatarHora(voo.estimated_arrival)"
        :destinationAirport="voo.destination_airport"
        :arrivalDateShort="formatarDataCurta(voo.estimated_arrival)"
        :totalSeats="voo.economy_seats + voo.business_seats + voo.first_seats"
        :businessSeats="voo.business_seats"
        :price="calcularPreco(voo)"
        :economySeats="voo.economy_seats"
        @selecionar="selecionarVoo"
    />
    </div>

    <!-- Nenhum voo encontrado -->
    <div v-else class="bg-grayScale-50 rounded-lg shadow-lg p-12 text-center">
      <Icon nameIcon="ExclamationTriangleIcon" class="w-16 h-16 text-grayScale-400 mx-auto mb-4" />
      <h3 class="text-xl font-bold text-grayScale-900 mb-2">Nenhum voo encontrado</h3>
      <p class="text-grayScale-600 mb-6">Tente ajustar seus filtros de busca</p>
      <button 
        @click="router.push('/')"
        class="bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg font-semibold transition-colors"
      >
        Nova busca
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["rota-autenticada"],
});

const router = useRouter();
const route = useRoute();
const toast = useToast();

const voos = ref<any[]>([]);
const loading = ref(true);
const filtros = ref({
  origin_city: route.query.origin_city as string || '',
  destination_city: route.query.destination_city as string || '',
  departure_date: route.query.departure_date as string || '',
});

// Mock de companhias aéreas
const airlines = {
  1: { name: 'LATAM', code: 'LA' },
  2: { name: 'GOL', code: 'G3' },
  3: { name: 'Azul', code: 'AD' },
};

function getAirlineName(airlineId: number) {
  return airlines[airlineId as keyof typeof airlines]?.name || 'Companhia Aérea';
}

function formatarHora(datetime: string) {
  return new Date(datetime).toLocaleTimeString('pt-BR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

function formatarData(datetime: string) {
  return new Date(datetime).toLocaleDateString('pt-BR');
}

function formatarDataCurta(datetime: string) {
  return new Date(datetime).toLocaleDateString('pt-BR', { 
    day: '2-digit', 
    month: 'short' 
  });
}

function calcularDuracao(saida: string, chegada: string) {
  const diff = new Date(chegada).getTime() - new Date(saida).getTime();
  const horas = Math.floor(diff / (1000 * 60 * 60));
  const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${horas}h ${minutos}min`;
}

function calcularPreco(voo: any) {
  // Preço mockado baseado na duração e assentos
  const basePrice = 250;
  const duration = (new Date(voo.estimated_arrival).getTime() - new Date(voo.departure_time).getTime()) / (1000 * 60 * 60);
  const price = basePrice + (duration * 30);
  return price.toFixed(2);
}

function selecionarVoo(voo: any) {
  router.push(`/voos/${voo.id}`)
}

// Buscar voos ao montar componente
onMounted(async () => {
  const queryParams = {
    origin_city: filtros.value.origin_city,
    destination_city: filtros.value.destination_city,
    departure_date: filtros.value.departure_date
  };

  const { data, error, execute } = useApi('get', '/flights/', { params: queryParams });

  await execute();
  
  loading.value = false;

  if (data.value && !error.value) {
    voos.value = data.value;
  } else {
    toast.error({ mensagem: 'Erro ao buscar voos' });
  }
});
</script>