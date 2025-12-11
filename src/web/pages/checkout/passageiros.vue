<template>
  <div class="min-h-screen pb-32 md:pb-10 relative">
    <div class="max-w-7xl mx-auto ">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Main Form Column -->
        <div class="flex-1 flex flex-col gap-3">
          <div class="bg-white rounded-lg shadow-sm border border-grayScale-200 overflow-hidden">
            <div class="p-4 border-b border-grayScale-200 flex justify-between items-center">
              <div class="flex items-center gap-2">
                <BackButton />
                <h2 class="text-xl font-bold text-grayScale-900">Passageiro</h2>
              </div>
              <Icon nameIcon="UserIcon" class="w-5 h-5 text-grayScale-500" />
            </div>
            
            <div class="p-4 pb-0 flex flex-col gap-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Nome"
                  tipoDeComponente="text"
                  tipoDeInput="text"
                  propriedade="firstName"
                  :valorVmodel="store.passenger.firstName"
                  @emiteValor="val => store.updatePassenger({ firstName: val })"
                  :obrigatorio="true"
                />
                <Input
                  label="Sobrenome"
                  tipoDeComponente="text"
                  tipoDeInput="text"
                  propriedade="lastName"
                  :valorVmodel="store.passenger.lastName"
                  @emiteValor="val => store.updatePassenger({ lastName: val })"
                  :obrigatorio="true"
                />
              </div>
              
              <Input
                label="Número do Documento CPF"
                tipoDeComponente="text"
                tipoDeInput="text"
                propriedade="document"
                placeholder="Ex: 123.456.789-00"
                :valorVmodel="store.passenger.document"
                @emiteValor="val => store.updatePassenger({ document: val })"
                :obrigatorio="true"
              />
              
              <Input
                label="Data de Nascimento"
                tipoDeComponente="date"
                tipoDeInput="date"
                propriedade="birthDate"
                :valorVmodel="store.passenger.birthDate"
                @emiteValor="val => store.updatePassenger({ birthDate: val })"
                :obrigatorio="true"
              />
            </div>
          </div>

          <!-- Ticket Class Selection -->
          <div class="bg-white rounded-lg shadow-sm border border-grayScale-200 p-4">
            <h3 class="text-lg font-bold text-grayScale-900 mb-4">Escolha seu tipo de assento</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
               <!-- Economy Card -->
               <div 
                 @click="store.setTicketClass('economy')"
                 class="border-2 rounded-lg p-4 cursor-pointer transition-all flex flex-col gap-2 relative"
                 :class="store.ticketClass === 'economy' ? 'border-primary bg-primary/5' : 'border-grayScale-200 hover:border-primary/50'"
               >
                 <div class="flex justify-between items-center">
                    <span class="font-bold text-grayScale-900">Econômica</span>
                    <div v-if="store.ticketClass === 'economy'" class="bg-primary rounded-full p-1">
                        <Icon nameIcon="CheckIcon" class="w-4 h-4 text-white" />
                    </div>
                 </div>
                 <p class="text-xs text-grayScale-600">Bagagem de mão incluída. Seleção de assentos padrão.</p>
                 <p class="font-bold text-lg text-primary mt-2">
                    R$ {{ getPrice('economy') }}
                 </p>
               </div>

               <!-- Premium Card -->
               <div 
                 @click="store.setTicketClass('premium')"
                 class="border-2 rounded-lg p-4 cursor-pointer transition-all flex flex-col gap-2 relative"
                 :class="store.ticketClass === 'premium' ? 'border-purple-600 bg-purple-50' : 'border-grayScale-200 hover:border-purple-300'"
               >
                 <div class="flex justify-between items-center">
                    <span class="font-bold text-grayScale-900 flex items-center gap-1">
                        <Icon nameIcon="StarIcon" class="w-4 h-4 text-yellow-500" />
                        Premium
                    </span>
                    <div v-if="store.ticketClass === 'premium'" class="bg-purple-600 rounded-full p-1">
                        <Icon nameIcon="CheckIcon" class="w-4 h-4 text-white" />
                    </div>
                 </div>
                 <p class="text-xs text-grayScale-600">Mais espaço, embarque prioritário e bagagem despachada.</p>
                 <p class="font-bold text-lg text-purple-700 mt-2">
                    R$ {{ getPrice('premium') }}
                 </p>
               </div>
            </div>
          </div>
        </div>

        <!-- Desktop Summary (Side) -->
        <div class="hidden lg:block w-80">
            <div class="bg-white rounded-lg shadow-lg p-6 sticky top-6">
                <h3 class="font-bold text-lg mb-4">Resumo da Compra</h3>
                <div class="flex flex-col gap-3 text-sm text-grayScale-600 border-b border-grayScale-200 pb-4 mb-4">
                    <div class="flex justify-between">
                        <span>Voos ({{ store.selectionParams.origin_city }} - {{ store.selectionParams.destination_city }})</span>
                    </div>
                    <div class="flex justify-between font-medium">
                         <span>Passageiro 1 ({{ store.ticketClass === 'economy' ? 'Econômica' : 'Premium' }})</span>
                         <span>R$ {{ store.totalPrice }}</span>
                    </div>
                </div>
                <div class="flex justify-between items-center mb-6">
                    <span class="font-bold text-grayScale-900">Total</span>
                    <span class="font-bold text-2xl text-primary">R$ {{ store.totalPrice }}</span>
                </div>
                <button 
                    @click="avancar"
                    class="w-full bg-primary hover:bg-primary-dark text-white py-3 rounded-lg font-bold transition-colors"
                >
                    Avançar para assentos
                </button>
            </div>
        </div>
      </div>
    </div>

    <!-- Mobile Summary (Fixed Bottom) -->
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-grayScale-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] p-4 z-50">
        <div class="flex flex-col gap-2">
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
             
             <div v-if="mobileDetailsOpen" class="text-sm text-grayScale-600 py-2 border-b border-grayScale-100 mb-2">
                 <div class="flex justify-between">
                     <span>Tarifa {{ store.ticketClass === 'economy' ? 'Econômica' : 'Premium' }}</span>
                     <span>R$ {{ store.totalPrice }}</span>
                 </div>
             </div>

             <button 
                @click="avancar"
                class="w-full bg-primary hover:bg-primary-dark text-white py-3 rounded-lg font-bold transition-colors"
            >
                Avançar para seleção de assentos
            </button>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';

definePageMeta({
  middleware: ["rota-autenticada"],
});

const store = useStoreVoos();
const router = useRouter();
const mobileDetailsOpen = ref(false);

function getPrice(cls: 'economy' | 'premium') {
    let total = 0;
    if (store.outboundFlight) total += store.outboundFlight.tickets?.[cls] || 0;
    if (store.inboundFlight) total += store.inboundFlight.tickets?.[cls] || 0;
    return total;
}

function avancar() {
    // Basic validation
    if(!store.passenger.firstName || !store.passenger.lastName || !store.passenger.document) {
        // TODO: Show toast
        return;
    }
    router.push('/checkout/assentos');
}
</script>
