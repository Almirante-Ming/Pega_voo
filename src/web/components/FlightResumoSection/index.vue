<template>
  <div class="mb-6">
      <div class="flex flex-col gap-2 mb-2">
        <div class="bg-primary text-white w-fit px-2 py-0.5 rounded text-xs font-bold uppercase">{{ type }}</div>
        <div class="flex items-center gap-2 font-bold">
            <span>{{ origin }}</span>
            <Icon nameIcon="ArrowRightIcon" class="w-4 text-grayScale-500" /> 
            <span> {{ destination }}</span>
        </div>
      </div>
      
      <FlightSummaryCard 
          :airline="flight.airline_name"
          :flightNumber="flight.flight_number"
          :departureTime="flight.departure_time"
          :seat="seat"
          :ticketClass="ticketClass"
      />
  </div>
</template>

<script setup lang="ts">
import Icon from '@/components/Icon/index.vue';
import FlightSummaryCard from '@/components/FlightSummaryCard/index.vue';

defineProps<{
    type: string; // 'Ida' | 'Volta'
    origin: string;
    destination: string;
    flight: any; // Ideally strictly typed
    seat: string;
    ticketClass: string;
}>();
</script>
