<template>
  <div class="max-w-md mx-auto space-y-4">
    <div class="flex items-center gap-2">
        <BackButton />
        <h1 class="text-lg font-bold text-grayScale-900">Detalhes do voo</h1>
    </div>
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">

        <div class="flex gap-1.5 justify-between mb-3">
            <div class="flex gap-2 items-center">
                 <div class="bg-primary rounded-full flex items-center justify-center p-2">
                    <Icon nameIcon="GlobeAltIcon" class="w-6 h-6 text-grayScale-50 rotate-45" />
                 </div>
                <span class="font-semibold text-grayScale-900">{{ voo.airline_name }}</span>
            </div>
        </div>




      <div class="flex items-center justify-between mb-2 text-center">
        <div class="flex flex-col items-center justify-center">
          <img src="/images/plane-takeoff.svg">
          <p class="text-lg font-bold">{{ formatarHora(voo.departure_time) }}</p>
          <p class="text-sm text-grayScale-700 max-w-[120px] md:max-w-[240px]">{{ voo.origin_city }}/{{ voo.origin_airport }}</p>
        </div>
        <div class="text-center flex-1">
            <hr class="border-grayScale-400"></hr>
            <p class="text-xs text-grayScale-600">{{ calcularDuracao(voo.departure_time, voo.estimated_arrival) }}</p>
            <p class="text-xs text-grayScale-600 mt-1">
              {{ voo.stops_count === 0 ? 'Direto' : `${voo.stops_count} parada(s)` }}
            </p>
        </div>
        <div class="flex flex-col items-center justify-center">
          <img src="/images/plane-landing.svg">
          <p class="text-lg font-bold">{{ formatarHora(voo.estimated_arrival) }}</p>
          <p class="text-sm text-grayScale-700 max-w-[120px] md:max-w-[240px]">{{ voo.destination_city }}/{{ voo.destination_airport }}</p>
        </div>
      </div>
      <div class="flex items-center justify-between text-xs text-grayScale-600">
      </div>
    </div>

    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">
      <h3 class="font-bold mb-2">Detalhes da Tarifa</h3>
      <div class="flex flex-col gap-2.5 text-sm">
        <div v-if="voo.tickets?.economy" class="flex justify-between items-center">
          <span>Preço Econômica</span>
          <div class="text-end">
            <span class="font-semibold text-grayScale-900">R$ {{ voo.tickets.economy }}</span>
            <p class="text-xs text-grayScale-500">{{ voo.avaliable_seats }} assentos disponíveis</p>
          </div>
        </div>
        <div v-if="voo.tickets?.premium" class="flex justify-between items-center">
          <span>Preço Premium</span>
          <div class="text-end">
            <span class="font-semibold text-grayScale-900">R$ {{ voo.tickets.premium }}</span>
            <p class="text-xs text-grayScale-500">{{ voo.premium_seats }} assentos disponíveis</p>
          </div>
        </div>
        
        <div class="flex justify-between mt-2 pt-2 border-t border-grayScale-300 text-xs text-grayScale-500">
            <span>Taxas e encargos inclusos</span>
        </div>
      </div>
    </div>

    <button
      class="w-full bg-primary hover:bg-primary-dark text-grayScale-50 px-6 py-3 rounded-lg font-semibold transition-colors mt-4"
      @click="acaoPrincipal"
    >
      {{ labelBotao }}
    </button>
  </div>
</template>

<script setup lang="ts">
// filepath: c:\Users\ext.gersonbjf\Documents\projetos\task_fly\src\web\pages\voos\[id].vue
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted, computed } from 'vue'
import { useApi } from '@/composables/useApi'
import BackButton from "@/components/BackButton/index.vue";
import { useStoreVoos } from '@/store/useStoreVoos'

const route = useRoute()
const router = useRouter()
const storeVoos = useStoreVoos()
const voo = ref<any>({})
const loading = ref(true)

const selectionMode = computed(() => route.query.selectionMode as string)

const labelBotao = computed(() => {
    if (selectionMode.value === 'outbound') return 'Selecionar este voo de Ida'
    if (selectionMode.value === 'inbound') return 'Selecionar este voo de Volta'
    return 'Continuar'
})

function acaoPrincipal() {
    if (selectionMode.value === 'outbound') {
        storeVoos.setOutboundFlight(voo.value)
        router.push('/voos/selecao-viagem')
    } else if (selectionMode.value === 'inbound') {
        storeVoos.setInboundFlight(voo.value)
        router.push('/voos/selecao-viagem')
    } else {
        // Fluxo normal (somente ida)
        storeVoos.setOutboundFlight(voo.value)
        storeVoos.setInboundFlight(null)
        router.push('/checkout/passageiros')
    }
}

function formatarHora(datetime: string) {
    if (!datetime) return ''
  return new Date(datetime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function calcularDuracao(saida: string, chegada: string) {
  const diff = new Date(chegada).getTime() - new Date(saida).getTime()
  const horas = Math.floor(diff / (1000 * 60 * 60))
  const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  return `${horas}h ${minutos}min`
}

function continuar() {
  // Navegar para página de passageiros ou checkout
  router.push('/checkout/passageiros')
}

onMounted(async () => {
  const { data, error, execute } = useApi('get', `/flights/${route.params.id}`)
  await execute()
  loading.value = false
  if (data.value && !error.value) {
    voo.value = data.value
  }
})
</script>