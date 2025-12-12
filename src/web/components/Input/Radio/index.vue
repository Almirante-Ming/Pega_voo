<template>
  <div v-if="visivel" class="mb-5 px-6">
    <label
      v-if="props.label"
      for="default-input"
      class="mb-3 block font-medium text-white "
    >
      {{ props.label }}
    </label>
    <div class="grid grid-cols-3 w-full justify-center">
      <div
        v-for="(opcao, index) in model"
        :key="index"
        :class="clsx('items-center mb-4', {
          'opacity-[0.55] ': !habilitado,
        })"
      >
        <input
          :id="'radio-' + index"
          type="radio"
          :value="opcao.chave"
          name="default-radio"
          :disabled="!habilitado"
          :class="clsx(
            'w-4 h-4  ring-offset-grayScale-800 focus:outline-none bg-grayScale-700 border-grayScale-600',
            {
              'cursor-not-allowed': !habilitado,
            }
          )"
          @change="emitSelectedValue(opcao.chave)"
        />
        <label
          :for="'radio-' + index"
          :class="clsx('ms-2 text-sm font-medium text-grayScale-100', {
            'cursor-not-allowed': !habilitado,
          })"
          >{{ opcao.descricao }}</label
        >
      </div>
    </div>

    <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
  </div>
</template>

<script setup lang="ts">
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
    visivel: true,
    habilitado: true,
    obrigatorio: false
  });

  const emits = defineEmits(['inputEmitValue']);

  function emitSelectedValue(chave: string) {
    emits('inputEmitValue', chave);
  }
</script>

<style scoped></style>
