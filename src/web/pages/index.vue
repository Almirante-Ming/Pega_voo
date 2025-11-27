<template>
  <div class="w-full bg-grayScale-50 rounded-lg shadow-lg p-4 px-5">
    <h1 class="text-2xl font-bold mb-6 text-grayScale-900">Passagens aéreas</h1>

    <!-- Tipo de viagem -->
    <div class="flex gap-1.5 mb-6 bg-grayScale-200 rounded-lg p-2 py-1">
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

    <span v-if="tipoViagem == 'multitrecho'" class="text-red-500"> Ainda não temmm </span>

    <!-- Formulário -->
    <div class="grid grid-cols-2 gap-2">
      <Input 
        v-for="campo in formularioFiltrado"
        :class="clsx({ 'col-span-2' : campo.propriedade != 'passageiros' && campo.propriedade != 'classe' })"
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
  middleware: ["rota-autenticada"],
});

const router = useRouter();
const toast = useToast();

const tipoViagem = ref('ida-volta');
const loading = ref(false);

const tiposViagem = [
  { valor: 'ida-volta', label: 'Ida e volta' },
  { valor: 'somente-ida', label: 'Somente ida' },
  { valor: 'multitrecho', label: 'Multitrecho' }
];

const formulario: Campo[] = [
  {
    label: "Origem",
    tipoDeDado: "string",
    propriedade: "origin_city",
    tipoDeInput: "string",
    obrigatorio: false,
    placeholder: "Cidade ou aeroporto"
  },
  {
    label: "Destino",
    tipoDeDado: "string",
    propriedade: "destination_city",
    tipoDeInput: "string",
    obrigatorio: false,
    placeholder: "Cidade ou aeroporto"
  },
  {
    label: "Data de ida",
    propriedade: "departure_date",
    tipoDeInput: "timestamp",
    validacao: "data",
    obrigatorio: false,
  },
  {
    label: "Data de volta",
    propriedade: "return_date",
    tipoDeInput: "timestamp",
    validacao: "data",
    obrigatorio: false,
  },
  {
    label: "Passageiros",
    propriedade: "passageiros",
    tipoDeInput: "select",
    modelType: "static" as const,
    obrigatorio: false,
    placeholder: "Selecione",
    model: [
      { chave: "1", descricao: "1 Passageiro" },
      { chave: "2", descricao: "2 Passageiros" },
      { chave: "3", descricao: "3 Passageiros" }
    ]
  },
  {
    label: "Classe",
    propriedade: "classe",
    tipoDeInput: "select",
    modelType: "static" as const,
    obrigatorio: false,
    placeholder: "Selecione",
    model: [
      { chave: "economica", descricao: "Econômica" },
      { chave: "executiva", descricao: "Executiva" },
      { chave: "primeira", descricao: "Primeira Classe" }
    ]
  }
];

const formularioFiltrado = computed(() => {
  if (tipoViagem.value === 'somente-ida') {
    return formulario.filter(campo => campo.propriedade !== 'return_date');
  }
  return formulario;
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

async function buscarVoos() {
  validarFormulario();
  
  // Valida se pelo menos origem OU destino está preenchido
  if (!form.value.origin_city && !form.value.destination_city) {
    toast.error({ mensagem: 'Preencha pelo menos a origem ou o destino' });
    return;
  }

  const queryParams = {
    origin_city: form.value.origin_city,
    destination_city: form.value.destination_city,
    departure_date: form.value.departure_date
  };

  loading.value = true;

  // Redireciona para página de voos com os parâmetros
  await router.push({
    path: '/voos',
    query: queryParams
  });

  loading.value = false;
}
</script>

<style scoped>
</style>