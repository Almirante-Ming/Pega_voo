<template>
  <div class="w-full bg-grayScale-50 rounded-lg shadow-lg p-4 px-5">
    <div class="flex items-center gap-2 mb-5">
      <img src="/images/plane-takeoff.svg" class="w-8 h-8 dark:bg-grayScale-900 rounded-full p-1"/>
      <h1 class="text-2xl font-bold text-grayScale-900">Passagens aéreas</h1>
    </div>

    <!-- Tipo de viagem -->
    <div class="flex gap-1.5 mb-3.5 bg-grayScale-200 rounded-lg p-2 py-1">
      <button 
        v-for="tipo in tiposViagem" 
        :key="tipo.valor"
        @click="tipoViagem = tipo.valor"
        class="flex-1 p-2 rounded-lg text-sm font-medium transition-colors"
        :class="tipoViagem === tipo.valor 
          ? 'bg-grayScale-50 shadow-sm text-grayScale-900' 
          : 'text-grayScale-700'"
      >
        {{ tipo.label }}
      </button>
    </div>

    <!-- Formulário -->
    <div class="flex flex-col gap-1">
      <Input 
        v-for="campo in formularioFiltrado"
        :key="campo.propriedade"
        :tipoDeComponente="campo.tipoDeInput"
        :tipoDeInput="campo.tipoDeInput"
        :label="campo.label"
        :propriedade="campo.propriedade"
        :model="campo.model"
        :modelType="campo.modelType"
        :obrigatorio="campo.obrigatorio"
        :placeholder="campo.placeholder"
        :tipoDeDado="campo.tipoDeDado"
        :hasError="Boolean(erros[campo.propriedade])"
        :errorMessage="erros[campo.propriedade]"
        :mostrarHora="false"
        @emiteValor="atualizarForm(campo.propriedade, $event, campo?.validacao)"
      />
    </div>

    <!-- Botão Buscar -->
    <div class="w-full mt-6">
      <button 
        :disabled="loading" 
        class="bg-primary hover:opacity-90 disabled:bg-grayScale-500 w-full rounded-lg text-white h-12 shadow-lg flex justify-center items-center font-semibold transition-all"
        @click="buscarVoos"
      >
        <Icon v-if="loading" nameIcon="ArrowPathIcon" class="text-white animate-spin mr-2"></Icon>
        <Icon v-else nameIcon="MagnifyingGlassIcon" class="text-white mr-2 w-5 h-5"></Icon>
        <span>{{ loading ? 'Buscando...' : 'Buscar voos' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { Campo } from "~/types/formulario";
import clsx from 'clsx'

definePageMeta({

});

const router = useRouter();
const toast = useToast();

const tipoViagem = ref('ida-volta');
const loading = ref(false);

const tiposViagem = [
  { valor: 'ida-volta', label: 'Ida e volta' },
  { valor: 'somente-ida', label: 'Somente ida' }
];

const formulario = computed<Campo[]>(() => [
  {
    label: "Origem",
    tipoDeDado: "string",
    propriedade: "origin_city",
    tipoDeInput: "string",
    obrigatorio: true,
    placeholder: "Cidade ou aeroporto"
  },
  {
    label: "Destino",
    tipoDeDado: "string",
    propriedade: "destination_city",
    tipoDeInput: "string",
    obrigatorio: true,
    placeholder: "Cidade ou aeroporto"
  },
  {
    label: "Data de ida",
    propriedade: "departure_date",
    tipoDeInput: "timestamp",
    mostrarHora: true,
    validacao: "data",
    obrigatorio: true,
  },
  {
    label: "Data de volta",
    propriedade: "return_date",
    tipoDeInput: "timestamp",
    mostrarHora: true,
    validacao: "data",
    obrigatorio: tipoViagem.value === 'ida-volta',
  },

]);

const formularioFiltrado = computed(() => {
  if (tipoViagem.value === 'somente-ida') {
    return formulario.value.filter(campo => campo.propriedade !== 'return_date');
  }
  return formulario.value;
});

const camposObrigatorios = computed(() => {
  return formularioFiltrado.value
    .filter(campo => campo.obrigatorio)
    .map(campo => campo.propriedade);
});

const camposOpcionais = computed(() => {
  return formularioFiltrado.value
    .filter(campo => !campo.obrigatorio)
    .map(campo => campo.propriedade);
});

const { form, erros, formValido, validarCampo, validarFormulario } = useForm(camposObrigatorios.value, camposOpcionais.value);

const atualizarForm = atualizarFormulario(form, validarCampo);

// Importar store
import { useStoreVoos } from '@/store/useStoreVoos';
const storeVoos = useStoreVoos();

async function buscarVoos() {
  // Força validação de todos os campos
  validarFormulario();

  // Lógica de validação personalizada porque useForm não é reativo a mudanças de modo
  if (tipoViagem.value === 'ida-volta') {
      if (!formValido.value) return;
  } else {
      // Somente ida: verificar campos obrigatórios manualmente e ignorar erro de data de volta
      const required = ['origin_city', 'destination_city', 'departure_date'];
      const hasEmpty = required.some(field => !form.value[field]);
      const hasError = required.some(field => erros.value[field]);
      
      if (hasEmpty || hasError) {
          toast.error({ mensagem: 'Preencha os campos obrigatórios' });
          return;
      }
  }

  // Valida campos obrigatórios de negócio extras - redundante mas seguro
  if (!form.value.origin_city || !form.value.destination_city || !form.value.departure_date) {
    toast.error({ mensagem: 'Preencha os campos obrigatórios' });
    return;
  }
  
  if (tipoViagem.value === 'ida-volta' && !form.value.return_date) {
      toast.error({ mensagem: 'Preencha a data de volta' });
      return;
  }

  loading.value = true;

  try {
      if (tipoViagem.value === 'ida-volta') {
          // Salva parametros na store e redireciona para o Hub
          storeVoos.setSelectionParams({
              origin_city: form.value.origin_city,
              destination_city: form.value.destination_city,
              departure_date: form.value.departure_date,
              return_date: form.value.return_date
          });
          // Limpa seleções anteriores para não misturar
          storeVoos.setOutboundFlight(null);
          storeVoos.setInboundFlight(null);

          await router.push('/voos/selecao-viagem');

      } else {
          // Somente ida - fluxo normal
          const queryParams = {
            origin_city: form.value.origin_city,
            destination_city: form.value.destination_city,
            departure_date: form.value.departure_date
          };
          
          await router.push({
            path: '/voos',
            query: queryParams
          });
      }
  } catch (e) {
      console.error(e);
      toast.error({ mensagem: 'Erro ao processar busca' });
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
</style>