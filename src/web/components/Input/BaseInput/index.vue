<template>
  <div v-if="visivel" class="mb-4">
    <label v-if="props.label" for="default-input" class="mb-1 block font-medium text-grayScale-800">{{ props.label }}
    </label>
    <input v-model="valueInput" @input="handleInput($event)" @keydown="handleInput($event)"
      @keydown.enter.prevent="$event.preventDefault()" @focusout="handleInput($event)" @focus="handleInputFocus"
      @blur="handleInputBlur" :maxLength="props.maxLength" :type="inputType" :valorPadrao="props.valorPadrao"
      :placeholder="placeholder" :disabled="!habilitado" autocomplete="off" :class="clsx(
        'custom-number-input block w-full rounded-lg p-2.5 text-sm text-grayScale-800 placeholder:text-grayScale-450 bg-input-100 border border-input-200 focus:border-primary focus:ring-primary',
        {
          'cursor-not-allowed opacity-[0.55]': !habilitado,
          'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
          'ring-[0.0600rem] ring-primary': isInputFocused && !hasError,
          'block w-full rounded-lg p-2.5 text-sm':
            inputType != 'file',
        }
      )
        " />

    <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
  </div>
</template>

<script setup lang="ts">
import { format } from "@/utils";
import clsx from "clsx";

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
  valoresNegativos?: boolean;
  tresCasasDecimais?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  tipoDeInput: String as PropType<Value>,
  habilitado: true,
  visivel: true,
  obrigatorio: false,
  valoresNegativos: false,
  tresCasasDecimais: false
});

const inputTypes = {
  senha: "password",
  number: "number",
  numberString: "text",
};

const placeholders = {
  cartao_de_credito: "0000 1111 2222 3333",
  cpf: "000.000.000-00",
  cpfCnpj: "000.000.000-00",
  email: "seuemail@email.com",
  cep: "00000-000",
  cnpj: "00.000.000/0000-00",
  telefone: "(00) 90000-0000",
  currency: "R$ 0,00",
  data: "dd/mm/aaaa",
};

const inputType = computed(() => {
  return inputTypes[props.tipoDeInput] || "text";
});

const placeholder = computed(() => {
  if (placeholders[props.tipoDeInput]) {
    return placeholders[props.tipoDeInput];
  } else {
    return props.placeholder;
  }
});

const emits = defineEmits(["inputEmitValue"]);

const valueInput = ref();

const campoDeNumero = [
  "cpf",
  "telefone",
  "cep",
  "cnpj",
  "cpfcnpj",
  "data",
  "cpfCnpj",
  "numberString",
  "int",
];

const campoDeLetra = ["uf", "email", "tag"];

const handleInput = (event: any, isFromApi = false) => {
  if (props.valoresNegativos && event.key === "-") {
    event.preventDefault();
  }
  if (props.tipoDeInput == "currency") {
    const valor = event.target.value ?? event;
    let formattedValue
    if (isFromApi) {
      const valorPadronizado = Number(valor).toFixed(2);
      formattedValue = formatCurrency(valorPadronizado, true);
    } else {
      const valorSemMascara = unformatCurrency(valor);
      formattedValue = formatCurrency(valorSemMascara);
    }
    emits(
      "inputEmitValue",
      formattedValue.replace(/[^\d,]/g, "").replace(",", ".")
    );
    valueInput.value = formattedValue;
    event.target.value = formattedValue; // Isso garante que o valor formatado seja exibido corretamente no input
  } else if (
    campoDeNumero.includes(props.tipoDeInput) &&
    typeof format[props.tipoDeInput] === "function"
  ) {
    const maskedValue = format[props.tipoDeInput](event.target.value);
    valueInput.value = maskedValue;

    if (props.tipoDeDado == "number")
      emits("inputEmitValue", parseInt(valueInput.value));
    else emits("inputEmitValue", valueInput.value.replace(/\D+/g, ""));
  } else if (
    campoDeLetra.includes(props.tipoDeInput) &&
    typeof format[props.tipoDeInput] === "function"
  ) {
    const maskedValue = format[props.tipoDeInput](event.target.value);
    valueInput.value = maskedValue;
    emits("inputEmitValue", valueInput.value);
  } else if (props.tipoDeInput == "codigo") {
    const maskedValue = format["codigo"](event.target.value);
    valueInput.value = maskedValue;
    emits("inputEmitValue", valueInput.value);
  } else {
    if (props.tipoDeDado == "number") {
      if (event.target.value)
        emits("inputEmitValue", parseFloat(event.target.value));
      else emits("inputEmitValue", event.target.value);
    } else emits("inputEmitValue", event.target.value);
  }
};

const campoObrigatorio = computed(() => {
  if (props.obrigatorio && valueInput.value) return true;
  else return false;
});

function unformatCurrency(value: any) {
  if (value == null) return "";
  return String(value).replace(/[^0-9]/g, "");
}

function formatCurrency(value: any, isFromApi = false): string {
  if (value === "" || value == null) return "";

  let number = typeof value === "string"
    ? parseFloat(value.replace(/[^0-9.-]+/g, ""))
    : value;

  if (!isFromApi) {
    // Apenas divide por 100 no caso de input do usuário
    number = typeof value === "string"
      ? parseFloat(value.replace(/[^0-9.-]+/g, "")) / 100
      : value;
  }

  if (isNaN(number)) return "";

  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(number);
}

const isInputFocused = ref(false);

const handleInputFocus = () => {
  isInputFocused.value = true;
};

const handleInputBlur = () => {
  isInputFocused.value = false;

  if (props.tresCasasDecimais && props.tipoDeDado === "number" && props.tipoDeInput === "number") {
    let valor = parseFloat(valueInput.value);

    if (!isNaN(valor)) {
      valor = Math.floor(valor * 1000) / 1000; // truncar para 3 casas
      valueInput.value = valor;
      emits("inputEmitValue", valor);
    }
  }
};

onMounted(() => {
  if (props.valorPadrao) {
    valueInput.value = props.valorPadrao;
    handleInput({ target: { value: valueInput.value } }, true);
  }
  if (props.valor) {
    valueInput.value = props.valor;
    handleInput({ target: { value: valueInput.value } }, true);
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