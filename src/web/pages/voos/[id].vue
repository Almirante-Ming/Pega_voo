<template>
  <div class="max-w-md mx-auto space-y-4">
    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">

        <div class="flex gap-1.5 justify-between mb-3">
            <div class="flex gap-2 items-center">
                <icon nameIcon="UserCircleIcon" class="size-9"></icon>
                <span class="bg-primary text-grayScale-50 px-3 py-0.5 rounded-full font-semibold">{{ getAirlineName(voo.airline_id) }}</span>
            </div>

            <div class="flex flex-col text-xs text-grayScale-700 items-end">
                <div class="flex gap-1.5 items-center"><icon nameIcon="PaperAirplaneIcon"/>{{ voo.aircraft_model }}</div>
                <p>Número do voo: {{ voo.flight_number }}</p>
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
      <h3 class="font-bold mb-2">Bagagem Incluída</h3>
      <div class="flex flex-col gap-2">
        <div>
          <Icon nameIcon="BriefcaseIcon" class="w-5 h-5 inline-block mr-1" />
          <strong>Bagagem de Mão</strong>
          <span class="ml-2">1 mala de mão (até 10kg) + 1 item pessoal</span>
        </div>
        <div>
          <Icon nameIcon="BriefcaseIcon" class="w-5 h-5 inline-block mr-1" />
          <strong>Bagagem Despachada</strong>
          <span class="ml-2">1 mala despachada (até 23kg)</span>
        </div>
      </div>
    </div>

    <div class="bg-grayScale-50 rounded-lg shadow-lg p-4">
      <h3 class="font-bold mb-2">Detalhes da Tarifa</h3>
      <div class="flex flex-col gap-1 text-sm">
        <div class="flex justify-between">
          <span>Tarifa Aérea</span>
          <span>R$ 1.050,00</span>
        </div>
        <div class="flex justify-between">
          <span>Taxas e Encargos</span>
          <span>R$ 150,00</span>
        </div>
        <div class="flex justify-between">
          <span>Seleção de Assento</span>
          <span>R$ 50,00</span>
        </div>
        <div class="flex justify-between font-bold mt-2">
          <span>Total</span>
          <span>R$ 1.250,00</span>
        </div>
      </div>
    </div>

    <button
      class="w-full bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-lg font-semibold transition-colors mt-4"
      @click="continuar"
    >
      Continuar
    </button>
  </div>
</template>

<script setup lang="ts">
// filepath: c:\Users\ext.gersonbjf\Documents\projetos\task_fly\src\web\pages\voos\[id].vue
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const route = useRoute()
const router = useRouter()
const voo = ref<any>({})
const loading = ref(true)

const airlines = {
  1: { name: 'LATAM', code: 'LA' },
  2: { name: 'GOL', code: 'G3' },
  3: { name: 'Azul', code: 'AD' },
}

function getAirlineName(airlineId: number) {
  return airlines[airlineId as keyof typeof airlines]?.name || 'Companhia Aérea'
}

function formatarHora(datetime: string) {
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
  router.push('/passageiros')
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