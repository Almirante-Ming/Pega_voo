<template>
  <div class="min-h-screen pb-32 md:pb-10 relative">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Main Form Column -->
        <div class="flex-1 flex flex-col gap-3">
          <div class="bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-300 overflow-hidden">
            <div class="p-4 border-b border-grayScale-300 flex justify-between items-center">
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
                  :valorVmodel="form.firstName"
                  @emiteValor="handleUpdate('firstName', $event)"
                  :obrigatorio="true"
                  :hasError="Boolean(erros.firstName)"
                  :errorMessage="erros.firstName"
                />
                <Input
                  label="Sobrenome"
                  tipoDeComponente="text"
                  tipoDeInput="text"
                  propriedade="lastName"
                  :valorVmodel="form.lastName"
                  @emiteValor="handleUpdate('lastName', $event)"
                  :obrigatorio="true"
                  :hasError="Boolean(erros.lastName)"
                  :errorMessage="erros.lastName"
                />
              </div>
              
              <Input
                label="Número do Documento CPF"
                tipoDeComponente="text"
                tipoDeInput="cpf"
                validacao="cpf"
                propriedade="document"
                :valorVmodel="form.document"
                @emiteValor="handleUpdate('document', $event, 'cpf')"
                :obrigatorio="true"
                :hasError="Boolean(erros.document)"
                :errorMessage="erros.document"
              />
              
              <Input
                label="Data de Nascimento"
                tipoDeComponente="date"
                tipoDeInput="date"
                validacao="data"
                propriedade="birthDate"
                :valorVmodel="form.birthDate"
                @emiteValor="handleUpdate('birthDate', $event, 'data')"
                :obrigatorio="true"
                :hasError="Boolean(erros.birthDate)"
                :errorMessage="erros.birthDate"
              />
            </div>
          </div>

          <!-- Ticket Class Selection -->
          <div class="bg-grayScale-50 rounded-lg shadow-sm border border-grayScale-300 p-4">
            <h3 class="text-lg font-bold text-grayScale-900 mb-4">Escolha seu tipo de assento</h3>
            
            <!-- Tabs for Round Trip -->
            <div v-if="store.inboundFlight" class="flex gap-2 mb-4 bg-grayScale-100 p-1 rounded-lg">
                <button 
                  @click="activeTab = 'ida'"
                  class="flex-1 py-2 text-sm font-bold rounded-md transition-colors"
                  :class="activeTab === 'ida' ? 'bg-grayScale-50 shadow text-primary' : 'text-grayScale-500 hover:text-grayScale-700'"
                >
                    Voo de Ida
                </button>
                <button 
                  @click="activeTab = 'volta'"
                  class="flex-1 py-2 text-sm font-bold rounded-md transition-colors"
                  :class="activeTab === 'volta' ? 'bg-grayScale-50 shadow text-primary' : 'text-grayScale-500 hover:text-grayScale-700'"
                >
                    Voo de Volta
                </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
               <!-- Economy Card -->
               <div 
                 @click="setCls('economy')"
                 class="border-2 rounded-lg p-4 cursor-pointer transition-all flex flex-col gap-2 relative"
                 :class="currentClass === 'economy' ? 'border-primary bg-primary/5' : 'border-grayScale-300 hover:border-primary/50'"
               >
                 <div class="flex justify-between items-center">
                    <span class="font-bold text-grayScale-900">Econômica</span>
                    <div v-if="currentClass === 'economy'" class="bg-primary rounded-full p-1">
                        <Icon nameIcon="CheckIcon" class="w-4 h-4 text-grayScale-50" />
                    </div>
                 </div>
                 <p class="text-xs text-grayScale-600">Bagagem de mão incluída. Seleção de assentos padrão.</p>
                 <p class="font-bold text-lg text-primary mt-2">
                    R$ {{ currentPrice('economy') }}
                 </p>
               </div>

               <!-- Premium Card -->
               <div 
                 @click="setCls('premium')"
                 class="border-2 rounded-lg p-4 cursor-pointer transition-all flex flex-col gap-2 relative"
                 :class="currentClass === 'premium' ? 'border-purple-600 bg-purple-50' : 'border-grayScale-300 hover:border-purple-300'"
               >
                 <div class="flex justify-between items-center">
                    <span class="font-bold text-grayScale-900 flex items-center gap-1">
                        <Icon nameIcon="StarIcon" class="w-4 h-4 text-yellow-500" />
                        Premium
                    </span>
                    <div v-if="currentClass === 'premium'" class="bg-purple-600 rounded-full p-1">
                        <Icon nameIcon="CheckIcon" class="w-4 h-4 text-grayScale-50" />
                    </div>
                 </div>
                 <p class="text-xs text-grayScale-600">Mais espaço, embarque prioritário e bagagem despachada.</p>
                 <p class="font-bold text-lg text-purple-700 mt-2">
                    R$ {{ currentPrice('premium') }}
                 </p>
               </div>
            </div>
          </div>
        </div>

        <!-- Summary Component -->
        <CheckoutSummary 
            buttonText="Avançar para assentos" 
            @submit="avancar" 
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStoreVoos } from '@/store/useStoreVoos';
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { GrupoFormulario } from "~/types/formulario";
import CheckoutSummary from '@/components/CheckoutSummary/index.vue';

definePageMeta({
  middleware: ["rota-autenticada"],
});

const store = useStoreVoos();
const router = useRouter();

const formulario: GrupoFormulario = [
    {
        title: "Dados Pessoais",
        columns: [
            {
                label: "Nome",
                propriedade: "firstName",
                tipoDeInput: "string",
                obrigatorio: true
            },
            {
                label: "Sobrenome",
                propriedade: "lastName",
                tipoDeInput: "string",
                obrigatorio: true
            },
            {
                label: "Documento",
                propriedade: "document",
                tipoDeInput: "cpf",
                validacao: "cpf",
                obrigatorio: true
            },
            {
                label: "Data de Nascimento",
                propriedade: "birthDate",
                tipoDeInput: "data",
                validacao: "data",
                obrigatorio: true
            }
        ]
    }
];

const camposObrigatorios = computed(() => {
    return formulario
        .flatMap(grupo => grupo.columns)
        .filter(campo => campo.obrigatorio)
        .map(campo => campo.propriedade);
});

const camposOpcionais = computed(() => {
    return formulario
        .flatMap(grupo => grupo.columns)
        .filter(campo => !campo.obrigatorio)
        .map(campo => campo.propriedade);
});

const { form, erros, formValido, validarCampo, validarFormulario } = useForm(camposObrigatorios.value, camposOpcionais.value);
const atualizarForm = atualizarFormulario(form, validarCampo);

// State for Tab Selection
const activeTab = ref<'ida' | 'volta'>('ida');

// Computed Class for the active tab
const currentClass = computed(() => {
    if (activeTab.value === 'ida') return store.outboundTicketClass;
    return store.inboundTicketClass;
});

function handleUpdate(prop: string, val: any, validationType?: string) {
    atualizarForm(prop, val, validationType);
    store.updatePassenger({ [prop]: val });
}

function setCls(cls: 'economy' | 'premium') {
    if (activeTab.value === 'ida') {
        store.setOutboundTicketClass(cls);
    } else {
        store.setInboundTicketClass(cls);
    }
}

function currentPrice(cls: 'economy' | 'premium') {
    if (activeTab.value === 'ida') {
        return store.outboundFlight?.tickets?.[cls] || 0;
    } else {
        return store.inboundFlight?.tickets?.[cls] || 0;
    }
}

function avancar() {
    validarFormulario();
    if (formValido.value) {
        router.push('/checkout/assentos');
    } else {
        // Optional: show toast
        console.log("Formulário inválido", erros.value);
    }
}

onMounted(() => {
    // Sync store data to form
    const currentPassenger = store.passenger;
    if (currentPassenger) {
        if(currentPassenger.firstName) form.value.firstName = currentPassenger.firstName;
        if(currentPassenger.lastName) form.value.lastName = currentPassenger.lastName;
        if(currentPassenger.document) form.value.document = currentPassenger.document;
        if(currentPassenger.birthDate) form.value.birthDate = currentPassenger.birthDate;
    }
});
</script>
