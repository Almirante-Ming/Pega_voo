<template>
  <div class="w-full space-y-4">
    <!-- Header com filtros -->
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
           <BackButton />
           <h2 class="text-xl font-bold text-grayScale-900">
             {{ voos.length ? voos.length : '' }} {{ voos.length == 0 ? 'Nenhum voo encontrado' : voos.length == 1 ? 'Voo encontrado' : 'Voos encontrados' }} 
            </h2>
        </div>
      </div>

      <!-- Info da busca -->
      <div class="flex flex-col gap-4 text-sm text-grayScale-700">
        <h2>Resumo da pesquisa</h2>

        <div class="flex gap-2 justify-around text-center capitalize">
          <span>
            <strong>Origem:</strong> {{ filtros.origin_city ? filtros.origin_city : 'Não informado' }}
          </span>
          <Icon nameIcon="ArrowRightIcon" class="w-5 h-5 self-center" />
          <span>
            <strong>Destino:</strong> {{ filtros.destination_city ? filtros.destination_city : 'Não informado' }}
          </span>
        </div>

        <span v-if="filtros.departure_date">
          <strong>Data:</strong> {{ formatarData(filtros.departure_date) }}
        </span>
      </div>
    </div>

    <!-- Carregando -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Icon nameIcon="ArrowPathIcon" class="w-8 h-8 text-primary animate-spin" />
    </div>

    <!-- Lista de voos -->
    <div v-else-if="voos.length > 0" class="space-y-3">
    <CardVoo
        v-for="voo in voos"
        :key="voo.id"
        :voo="voo"
        :airlineName="voo.airline_name"
        :flightNumber="voo.flight_number"
        :departureHour="formatarHora(voo.departure_time)"
        :originAirport="voo.origin_airport"
        :originCity="voo.origin_city"
        :departureDateShort="formatarDataCurta(voo.departure_time)"
        :duration="calcularDuracao(voo.departure_time, voo.estimated_arrival)"
        :arrivalHour="formatarHora(voo.estimated_arrival)"
        :destinationAirport="voo.destination_airport"
        :destinationCity="voo.destination_city"
        :arrivalDateShort="formatarDataCurta(voo.estimated_arrival)"
        :totalSeats="voo.economy_seats + voo.business_seats + voo.first_seats"
        :businessSeats="voo.business_seats"
        :economyPrice="voo.tickets?.economy"
        :premiumPrice="voo.tickets?.premium"
        :economySeats="voo.avaliable_seats"
        :premiumSeats="voo.premium_seats"
        :aircraftModel="voo.aircraft_model"
        @selecionar="selecionarVoo"
    />
    </div>

    <!-- Nenhum voo encontrado -->
    <div v-else class="bg-grayScale-50 rounded-lg shadow-lg p-12 text-center">
      <Icon nameIcon="ExclamationTriangleIcon" class="w-16 h-16 text-grayScale-400 mx-auto mb-4" />
      <h3 class="text-xl font-bold text-grayScale-900 mb-2">Nenhum voo encontrado</h3>
      <p class="text-grayScale-600 mb-6">Tente ajustar seus filtros de busca</p>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({

});
import BackButton from '@/components/BackButton/index.vue';

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

function formatarHora(datetime: string) {
  return new Date(datetime).toLocaleTimeString('pt-BR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

function formatarData(datetime: string) {
  if (!datetime) return '';
  if (datetime.includes('T')) {
      return new Date(datetime).toLocaleDateString('pt-BR');
  }
  const [year, month, day] = datetime.split('-');
  return `${day}/${month}/${year}`;
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

async function buscarVoos() {
  loading.value = true;
  try {
    const { data, execute } = useApi('get', '/flights/', {
      params: {
        origin_city: filtros.value.origin_city,
        destination_city: filtros.value.destination_city,
        departure_date: filtros.value.departure_date
      }
    });

    await execute();
    
    voos.value = data.value || [];
  } catch (error) {
    console.error('Erro ao buscar voos:', error);
    toast.error({ mensagem: 'Não foi possível carregar os voos.' });
  } finally {
    loading.value = false;
  }
}

function selecionarVoo(voo: any) {
  const selectionMode = route.query.selectionMode;

  if (selectionMode) {
      // Se estamos no modo de seleção (ida/volta), redireciona pro detalhes mantendo o modo
      router.push({
          path: `/voos/${voo.id}`,
          query: { selectionMode }
      });
  } else {
      // Fluxo padrão
      router.push(`/voos/${voo.id}`);
  }
}

onMounted(() => {
  if (filtros.value.origin_city && filtros.value.destination_city && filtros.value.departure_date) {
    buscarVoos();
  } else {
    loading.value = false;
  }
});
</script>