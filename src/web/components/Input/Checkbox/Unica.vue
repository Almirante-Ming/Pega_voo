<template>
  <div v-if="props.visivel">
    <div class="flex items-center" :class="clsx({'mb-4' : props.marginBottom})">
      <input
        :id="'checkbox-' + props.propriedade"
        type="checkbox"
        :disabled="!props.habilitado"
        @change="toggleCheckbox"
        :checked="checkboxStates.checked"
        class="w-[18px] h-[18px] text-primary rounded focus:ring-primary bg-grayScale-50 border-grayScale-400 focus:outline-none"
      />
      <label
        :for="'checkbox-' + props.propriedade"
        class="ms-2 font-medium text-grayScale-800 select-none"
      >
        {{ props.label }}
      </label>
    </div>
    <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import clsx from 'clsx';

interface Props {
  propriedade: string;
  label: string;
  tipoDeDado?: string;
  valorPadrao?: any;
  obrigatorio?: boolean;
  visivel?: boolean;
  errorMessage?: string;
  habilitado?: boolean;
  valor?: boolean;
  marginBottom?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  tipoDeDado: 'boolean',
  habilitado: true,
  visivel: true,
  obrigatorio: true,
  valor: false,
  marginBottom: true
});

const emits = defineEmits(['inputEmitValue']);

const checkboxStates = ref<{ checked: boolean }>({
  checked: props.valor ?? false,
});

watch(
  () => props.valor,
  (newValue) => {
    checkboxStates.value.checked = newValue ?? false;
  }
);

function toggleCheckbox(event: Event) {
  const target = event.target as HTMLInputElement;
  checkboxStates.value.checked = target.checked;
  emits('inputEmitValue', target.checked);
}

onMounted(()=> {
  checkboxStates.value.checked = props.valor ?? false
  emits('inputEmitValue', checkboxStates.value.checked)
})
</script>

<style scoped></style>