<template>
  <div class="bg-grayScale-50 rounded-lg shadow-lg p-4 hover:shadow-xl transition-shadow">
    <div class="flex flex-col gap-2.5">
      <!-- Informações do voo -->
      <div class="flex-1 w-full flex flex-col gap-4">
        <div class="flex items-center gap-4 mb-3">
          <div class="flex items-center gap-2">
            <div class="bg-primary rounded-full flex items-center justify-center p-1.5">
              <Icon nameIcon="GlobeAltIcon" class="w-5 h-5 text-white rotate-45" />
            </div>
            <div>
              <p class="font-semibold text-grayScale-900">{{ airlineName }}</p>
              <p class="text-xs text-grayScale-600">{{ flightNumber }}</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-6">
          <div class="text-center">
            <p class="text-2xl font-bold text-grayScale-900">{{ departureHour }}</p>
            <p class="text-sm text-grayScale-700">{{ originAirport }}</p>
            <p class="text-xs text-grayScale-600">{{ originCity }}</p>
            <p class="text-xs text-grayScale-600">{{ departureDateShort }}</p>
          </div>
          <div class="flex-1 px-4">
            <div class="relative">
              <div class="border-t-2 border-grayScale-300"></div>
              <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-grayScale-50 px-2">
                <Icon nameIcon="ClockIcon" class="w-4 h-4 text-grayScale-600" />
              </div>
            </div>
            <p class="text-xs text-center text-grayScale-600 mt-1">
              {{ duration }}
            </p>
            <p class="text-xs text-center text-grayScale-600">Direto</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-grayScale-900">{{ arrivalHour }}</p>
            <p class="text-sm text-grayScale-700">{{ destinationAirport }}</p>
            <p class="text-xs text-grayScale-600">{{ destinationCity }}</p>
            <p class="text-xs text-grayScale-600">{{ arrivalDateShort }}</p>
          </div>
        </div>

        <div class="flex flex-col gap-1 text-xs text-grayScale-600">
             <div class="flex items-center gap-1 ">
                 <Icon nameIcon="UserIcon" class="w-4 h-4" />
                 {{ economySeats }} assentos disponíveis
             </div>
             <div class="flex items-center gap-1 ">
                 <Icon nameIcon="StarIcon" class="w-4 h-4" />
                 {{ premiumSeats }} assentos premium
             </div>
        </div>
      </div>

      <!-- Divisor -->
      <hr class="border-grayScale-300" />

      <!-- Preço e botão -->
      <div class="w-full flex flex-col items-end">
        <div class="flex items-end gap-2.5 w-full justify-between">
            <div>
                <p class="text-xs text-grayScale-500">A partir de</p>
                <p class="text-xl font-bold text-primary">
                  {{ displayedPrice }}
                </p>
            </div>
            <button 
              @click="$emit('selecionar', voo)"
              class="bg-primary hover:bg-primary-dark text-white text-sm px-6 py-2 rounded-lg font-semibold transition-colors"
            >
              Selecionar
            </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  voo: any,
  airlineName: string,
  flightNumber: string,
  departureHour: string,
  originAirport: string,
  originCity: string,
  departureDateShort: string,
  duration: string,
  arrivalHour: string,
  destinationAirport: string,
  destinationCity: string,
  arrivalDateShort: string,
  totalSeats: number,
  businessSeats: number,
  economyPrice?: number,
  premiumPrice?: number,
  economySeats: number,
  premiumSeats: number,
  aircraftModel: string
}>();

defineEmits<{
  (e: 'selecionar', voo: any): void
}>();

const displayedPrice = computed(() => {
  const eco = props.economyPrice;
  const prem = props.premiumPrice;

  if (eco && prem) {
    return `R$ ${eco} ~ R$ ${prem}`;
  }
  if (eco) {
    return `R$ ${eco}`;
  }
  if (prem) {
    return `R$ ${prem}`;
  }
  return '...';
});
</script>