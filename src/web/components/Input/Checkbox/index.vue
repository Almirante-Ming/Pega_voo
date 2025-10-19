<template>
    <div v-if="visivel" class="mb-3">
      <label
        v-if="props.label"
        for="default-input"
        class="mb-3 block font-medium text-white"
      >
        {{ props.label }}
      </label>
      <div
        v-for="(opcao, index) in model"
        :key="index"
        :class="clsx('flex items-center mb-2', {
          'opacity-[0.55] ': !habilitado,
        })"
      >
        <input
          :id="'checkbox-' + index"
          type="checkbox"
          :disabled="!habilitado"
          @change="toggleCheckbox($event, opcao.chave)"
          :class="clsx(
            'w-4 h-4 text-primary rounded focus:ring-primary ring-offset-grayScale-800 bg-grayScale-700 border-grayScale-600 focus:outline-none',
            {
              'cursor-not-allowed': !habilitado,
            }
          )"
        />
        <label
          :for="'checkbox-' + index"
          :class="clsx('ms-2 text-sm font-medium text-grayScale-100', {
            'cursor-not-allowed': !habilitado,
          })"
        >
          {{ opcao.descricao }}
        </label>
      </div>
      <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch } from 'vue';
  import clsx from 'clsx';
  
  interface Opcao {
    descricao: string;
    chave: string;
  }
  
  interface Props {
    propriedade?: string;
    label?: string;
    model?: Opcao[];
    tipoDeDado?: string;
    valorPadrao?: any;
    obrigatorio?: boolean;
    visivel?: boolean;
    errorMessage?: string;
    habilitado?: boolean;
  }
  
  const props = withDefaults(defineProps<Props>(), {
    tipoDeDado: 'string',
    habilitado: true,
    visivel: true,
  });
  
  const emits = defineEmits(['inputEmitValue']);
  
  const checkboxStates = ref<{ [key: string]: boolean }>({});
  
  if (props.model) {
    props.model.forEach(opcao => {
      checkboxStates.value[opcao.chave] = false;
    });
  }
  
  function toggleCheckbox(event: Event, chave: string) {
    const target = event.target as HTMLInputElement;
    const isChecked = target.checked;
  
    checkboxStates.value[chave] = isChecked;
  
    emits('inputEmitValue', [checkboxStates.value]);
  }
  </script>
  
  <style scoped></style>
  