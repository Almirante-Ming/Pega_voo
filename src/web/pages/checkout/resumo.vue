<template>
  <div class="min-h-screen bg-grayScale-50 pb-10">
    <div class="max-w-4xl mx-auto p-3">
      <div class="flex items-center gap-2 mb-6">
        <BackButton />
        <h1 class="text-2xl font-bold text-grayScale-900">Resumo da Reserva</h1>
      </div>

      <div class="bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-300 overflow-hidden">
        <!-- Informações do Passageiro -->
        <div class="p-4 border-b border-grayScale-100">
            <h2 class="font-bold text-lg mb-4 text-grayScale-900">Dados do Passageiro</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-grayScale-700">
                <div>
                    <span class="block text-grayScale-500 text-xs">Nome Completo</span>
                    {{ store.passenger.firstName }} {{ store.passenger.lastName }}
                </div>
                <div>
                    <span class="block text-grayScale-500 text-xs">Documento</span>
                    {{ store.passenger.document }}
                </div>
            </div>
        </div>

        <!-- Voos -->
        <div class="p-4 border-b border-grayScale-100">
             <h2 class="font-bold text-lg mb-4 text-grayScale-900">Itinerário</h2>
             
             <!-- Ida -->
             <FlightResumoSection 
                v-if="store.outboundFlight"
                type="Ida"
                :origin="store.outboundFlight.origin_city"
                :destination="store.outboundFlight.destination_city"
                :flight="store.outboundFlight"
                :seat="store.selectedSeats[store.outboundFlight.id] || ''"
                :ticketClass="store.outboundTicketClass"
             />

             <!-- Volta -->
             <FlightResumoSection
                v-if="store.inboundFlight"
                type="Volta"
                :origin="store.inboundFlight.origin_city"
                :destination="store.inboundFlight.destination_city"
                :flight="store.inboundFlight"
                :seat="store.selectedSeats[store.inboundFlight.id] || ''"
                :ticketClass="store.inboundTicketClass"
             />
        </div>

        <!-- Total do Pagamento -->
        <div class="p-4 bg-grayScale-50">
            <div class="flex flex-col gap-2 mb-4 border-b border-grayScale-300 pb-4">
                <div v-if="store.outboundFlight" class="flex justify-between items-center text-sm">
                    <span class="text-grayScale-600">1 assento (Ida)</span>
                    <span class="font-semibold text-grayScale-900">R$ {{ store.outboundFlight.tickets?.[store.outboundTicketClass] }}</span>
                </div>
                <div v-if="store.inboundFlight" class="flex justify-between items-center text-sm">
                    <span class="text-grayScale-600">1 assento (Volta)</span>
                    <span class="font-semibold text-grayScale-900">R$ {{ store.inboundFlight.tickets?.[store.inboundTicketClass] }}</span>
                </div>
            </div>

            <div class="flex justify-between items-center mb-6">
                <span class="text-lg font-bold text-grayScale-900">Total</span>
                <span class="text-xl font-bold text-grayScale-900">R$ {{ store.totalPrice }}</span>
            </div>
            
            <button 
                @click="processPayment"
                :disabled="loading"
                class="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 rounded-lg shadow-sm flex justify-center items-center gap-2 transition-colors disabled:opacity-75 disabled:cursor-not-allowed"
            >
                <Icon v-if="!loading" nameIcon="CreditCardIcon" class="w-6 h-6" />
                <span v-if="!loading">Ir para Pagamento</span>
                <span v-else>Processando...</span>
            </button>
            <p v-if="error" class="text-red-500 text-sm mt-2 text-center">Ocorreu um erro ao iniciar o pagamento. Tente novamente.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';
import { useApi } from '@/composables/useApi';
import FlightResumoSection from '@/components/FlightResumoSection/index.vue';
import { useToast } from '@/composables/useToast';

definePageMeta({

});

const store = useStoreVoos();
const { execute, loading, data, error } = useApi('post', '/tickets/', {});
const { error: toastError } = useToast();

async function processPayment() {
    const flightsToBook = [];
    if (store.outboundFlight) {
        flightsToBook.push({
            flight_id: store.outboundFlight.id,
            seat_number: store.selectedSeats[store.outboundFlight.id]
        });
    }
    if (store.inboundFlight) {
        flightsToBook.push({
            flight_id: store.inboundFlight.id,
            seat_number: store.selectedSeats[store.inboundFlight.id]
        });
    }

    let paymentLink = '';

    for (const payload of flightsToBook) {
        try {
            await execute(payload);
            
            if (data.value && data.value.checkout_url) {
                 paymentLink = data.value.checkout_url;
            }
            
        } catch (e) {
            console.error(e);
            if(!error.value) toastError({ 
                titulo: 'Erro', 
                mensagem: 'Erro ao processar reserva.'
            });
            return; 
        }
    }

    if (paymentLink) {
        // Persistir detalhes do voo para página de sucesso
        if (store.outboundFlight) {
            localStorage.setItem('last_payment_flight', JSON.stringify(store.outboundFlight));
        }
        window.location.href = paymentLink;
    } else {
        console.warn("No payment link found in response", data.value);
        toastError({ 
            titulo: 'Erro', 
            mensagem: 'Link de pagamento não retornado.'
        });
    }
}
</script>
