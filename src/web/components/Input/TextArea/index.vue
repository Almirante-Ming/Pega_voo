<template>
  <div
    v-if="visivel"
    class="mb-4"
  >
    <label
      v-if="props.label"
      for="default-input"
      class="mb-1 block font-medium text-primary-theme"
      >{{ props.label }}
    </label>
    <textarea
      v-model="valueInput"
      @input="handleInput($event)"
      @keydown="handleInput($event)"
      @keydown.enter.prevent="$event.preventDefault()"
      @focusout="handleInput($event)"
      @focus="handleInputFocus"
      @blur="handleInputBlur"
      :maxLength="props.maxLength"
      :valorPadrao="props.valorPadrao"
      :placeholder="props.placeholder"
      :disabled="!habilitado"
      autocomplete="off"
      :class="
        clsx(
          'custom-number-input block w-full rounded-lg bg-input-theme border border-input-theme p-2.5 text-sm text-primary- min-h-[100px] max-h-[200px] focus:outline-none outline-none shadow-none',
          {
            'cursor-not-allowed opacity-[0.45]': !habilitado,
            'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
            'ring-[0.0600rem] ring-primary': isInputFocused && !hasError
          }
        )
    ">
    </textarea>

    <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
  </div>
</template>

<script setup lang="ts">
import clsx from "clsx";
import { format } from "@/utils";

interface Props {
  label?: string;
  tipoDeInput?: any; //cpf, data, select,
  tipoDeDado?: string; //number, string
  valorPadrao?: any;
  placeholder?: string;
  obrigatorio?: boolean;
  maxLength?: number;
  visivel?: boolean;
  hasSuccess?: boolean;
  hasError?: boolean;
  errorMessage?: any;
  habilitado?: boolean;
  propriedade?: string;
  valor?: any;
}

const props = withDefaults(defineProps<Props>(), {
  tipoDeInput: String as PropType<Value>,
  habilitado: true,
  visivel: true,
  obrigatorio: false
});


const emits = defineEmits(["inputEmitValue"]);

const valueInput = ref();



const handleInput = (event: any) => {
  emits("inputEmitValue", event.target.value);
};

const isInputFocused = ref(false);

const handleInputFocus = () => {
  isInputFocused.value = true;
};

const handleInputBlur = () => {
  isInputFocused.value = false;
};

onMounted(() => {
  if (props.valorPadrao) {
    valueInput.value = props.valorPadrao;
    handleInput({ target: { value: valueInput.value } });
  }
  if (props.valor) {
    valueInput.value = props.valor;
    handleInput({ target: { value: valueInput.value } });
  }
});
</script>

<style scoped>
input.custom-number-input[type="number"]::-webkit-inner-spin-button,
input.custom-number-input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Para Firefox */
input.custom-number-input[type="number"] {
  -moz-appearance: textfield;
}
</style>