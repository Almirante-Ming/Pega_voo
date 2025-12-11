<template>
  <div class="bg-grayScale-50 p-4 rounded-lg border border-grayScale-300">
      <p class="font-bold text-grayScale-900 flex items-center gap-2">
      <Icon nameIcon="GlobeAltIcon" class="w-4 h-4 -rotate-45 text-grayScale-700" />
      {{ airline }} 
      <span class="text-xs font-normal text-grayScale-500">(Voo {{ flightNumber }})</span>
      </p>
      <p class="text-sm mt-1">{{ formattedDate }}</p>
      <div class="mt-2 text-sm flex gap-4">
          <span><span class="font-semibold">Assento:</span> {{ seat }}</span>
          <span><span class="font-semibold">Classe:</span> {{ ticketClass === 'economy' ? 'Econômica' : 'Premium' }}</span>
      </div>
  </div>
</template>

<script setup lang="ts">
import Icon from '@/components/Icon/index.vue';

const props = defineProps<{
    airline: string;
    flightNumber: string;
    departureTime: string;
    seat: string;
    ticketClass: string;
}>();

const formattedDate = computed(() => {
    if(!props.departureTime) return '';
    return new Date(props.departureTime).toLocaleDateString('pt-BR', { 
        day: '2-digit', month: 'long', year: 'numeric', 
        hour: '2-digit', minute: '2-digit' 
    });
});
</script>
