<template>
  <div>
    <!-- Desktop Summary (Side) -->
    <div class="hidden lg:block w-80">
        <div class="bg-grayScale-50 rounded-lg shadow-lg p-6 sticky top-6">
            <h3 class="font-bold text-lg mb-4">Resumo da Compra</h3>
            <div class="flex flex-col gap-3 text-sm text-grayScale-600 border-b border-grayScale-300 pb-4 mb-4">
                <div class="flex justify-between">
                    <span>Voos ({{ store.selectionParams.origin_city }} - {{ store.selectionParams.destination_city }})</span>
                </div>
                <div class="flex flex-col gap-1 font-medium">
                     <div class="flex justify-between">
                        <span>Passageiro 1</span>
                        <span>R$ {{ store.totalPrice }}</span>
                     </div>
                     <div class="text-xs text-grayScale-500 font-normal flex flex-col gap-1 mt-1">
                        <div class="flex justify-between">
                            <span>Ida: {{ store.outboundTicketClass === 'economy' ? 'Econômica' : 'Premium' }}</span>
                            <span v-if="showSeats && store.selectedSeats[store.outboundFlight?.id]" class="font-medium text-grayScale-700">
                                Assento {{ store.selectedSeats[store.outboundFlight.id] }}
                            </span>
                        </div>
                        <div v-if="store.inboundFlight" class="flex justify-between">
                            <span>Volta: {{ store.inboundTicketClass === 'economy' ? 'Econômica' : 'Premium' }}</span>
                            <span v-if="showSeats && store.selectedSeats[store.inboundFlight?.id]" class="font-medium text-grayScale-700">
                                Assento {{ store.selectedSeats[store.inboundFlight.id] }}
                            </span>
                        </div>
                     </div>
                </div>
            </div>
            <div class="flex justify-between items-center mb-6">
                <span class="font-bold text-grayScale-900">Total</span>
                <span class="font-bold text-2xl text-primary">R$ {{ store.totalPrice }}</span>
            </div>
            <button 
                @click="$emit('submit')"
                :disabled="disabled"
                class="w-full bg-primary hover:bg-primary-dark disabled:bg-grayScale-400 text-grayScale-50 py-3 rounded-lg font-bold transition-colors"
                :class="{'opacity-75 cursor-not-allowed': disabled}"
            >
                {{ buttonText }}
            </button>
        </div>
    </div>

    <!-- Mobile Summary (Fixed Bottom) -->
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-grayScale-50 border-t border-grayScale-300 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] p-4 z-50">
        <div class="flex flex-col gap-4">
             <div 
               @click="mobileDetailsOpen = !mobileDetailsOpen"
               class="flex justify-between items-center cursor-pointer"
             >
                <div class="flex items-center gap-2">
                    <span class="font-bold text-grayScale-900">Total</span>
                    <Icon :nameIcon="mobileDetailsOpen ? 'ChevronDownIcon' : 'ChevronUpIcon'" class="w-4 h-4 text-grayScale-500" />
                </div>
                <span class="font-bold text-xl text-primary">R$ {{ store.totalPrice }}</span>
             </div>
             
             <div v-if="mobileDetailsOpen" class="text-sm text-grayScale-600 py-2 border-b border-grayScale-100">
                 <div class="flex justify-between">
                     <span class="font-medium">Ida ({{ store.outboundTicketClass === 'economy' ? 'Econômica' : 'Premium' }})</span>
                     <span>R$ {{ store.outboundFlight?.tickets?.[store.outboundTicketClass] }}</span>
                 </div>
                 <div v-if="showSeats && store.selectedSeats[store.outboundFlight?.id]" class="flex justify-end text-xs text-grayScale-500 mb-1">
                     Assento {{ store.selectedSeats[store.outboundFlight?.id] }}
                 </div>

                 <div v-if="store.inboundFlight" class="flex justify-between mt-1">
                     <span class="font-medium">Volta ({{ store.inboundTicketClass === 'economy' ? 'Econômica' : 'Premium' }})</span>
                     <span>R$ {{ store.inboundFlight?.tickets?.[store.inboundTicketClass] }}</span>
                 </div>
                 <div v-if="showSeats && store.inboundFlight && store.selectedSeats[store.inboundFlight.id]" class="flex justify-end text-xs text-grayScale-500">
                     Assento {{ store.selectedSeats[store.inboundFlight.id] }}
                 </div>
             </div>

             <button 
                @click="$emit('submit')"
                :disabled="disabled"
                class="w-full bg-primary hover:bg-primary-dark disabled:bg-grayScale-400 text-grayScale-50 py-3 rounded-lg font-bold transition-colors"
                :class="{'opacity-75 cursor-not-allowed': disabled}"
            >
                {{ buttonText }}
            </button>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';

const props = defineProps<{
    buttonText: string;
    disabled?: boolean;
    showSeats?: boolean;
}>();

defineEmits(['submit']);

const store = useStoreVoos();
const mobileDetailsOpen = ref(false);
</script>
