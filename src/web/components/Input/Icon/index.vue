<template>
	<div v-if="visivel" class="mb-5">
		<label v-if="props.label" for="default-input" class="mb-1 block font-medium text-grayScale-800">
			{{ props.label}}
		</label>
		<div :class="clsx({
			'cursor-not-allowed opacity-[0.55]': !habilitado,
			'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess && !isInputFocused,
			'ring-[0.0600rem] ring-primary ': isInputFocused,
			'ring-[0.0600rem] ring-[#22bb33]': !hasError && hasSuccess && !isInputFocused,
		}, 'flex w-full rounded-lg  text-sm text-primary items-center relative ')
			">
			<input v-model="valueInput" @input="handleInput($event)" @keydown="handleInput($event)"
				:maxlength="props.maxLength" @focusout="handleInput($event)" @focus="handleInputFocus"
				@blur="handleInputBlur" :type="inputType" @keydown.enter.prevent="$event.preventDefault()"
				:valorPadrao="props.valorPadrao" :placeholder="placeholder" :disabled="!habilitado" :class="clsx({
					'cursor-not-allowed opacity-[0.55]': !habilitado,
					'block w-full mb-5 text-sm  rounded-lg  border border-input-200 cursor-pointer text-grayScale-200 bg-grayScale-700 placeholder-grayScale-400':
						inputType == 'file',
					'block w-full rounded-lg border border-input-200 p-2.5 text-sm text-grayScale-800 placeholder:text-grayScale-450 bg-input-100 focus:!ring-0 focus:border-primary':
						inputType != 'file',
				})
					" />
			<div class=" absolute right-1 cursor-pointer flex justify-center text-grayScale-500 items-center"
				v-if="props.icone" @click="handleEvent">
				<Icon :name-icon="props.icone" class="size-5" />
			</div>
		</div>

		<span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
	</div>

</template>

<script setup lang="ts">
import { format } from "@/utils";
import clsx from "clsx";

const emits = defineEmits(["inputEmitValue", "emitClick"]);

const valueInput = ref();

const handleEvent = (event: any) => {
	emits("emitClick", event);
}

interface Props {
	label?: string;
	tipoDeInput?: any; //cpf, data,
	tipoDeDado?: string; //input, select
	valorPadrao?: any;
	placeholder?: string;
	obrigatorio?: boolean;
	maxLength?: number;
	visivel?: boolean;
	hasSuccess?: boolean;
	hasError?: boolean;
	errorMessage?: string;
	habilitado?: boolean;
	propriedade?: string;
	valor?: any;
	icone: any;
}

const props = withDefaults(defineProps<Props>(), {
	tipoDeDado: "string", //string, number, boolean
	tipoDeInput: String as PropType<Value>,
	habilitado: true,
	visivel: true,
	obrigatorio: false
});

const inputTypes = {
	radioButton: "radio",
	fileUpload: "file",
	senha: "password",
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
		return props.placeholder
	}
});

const campoDeNumero = [
	"cpf",
	"telefone",
	"cep",
	"cnpj",
	"cpfCnpj",
	"data",
	"cpfCnpj",
];

const campoDeLetra = ["uf"];

const handleInput = (event: any) => {
	if (props.tipoDeInput == "currency") {
		const valor = event.target.value ?? event;
		const formattedValue = formatCurrency(unformatCurrency(valor));
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
		emits("inputEmitValue", valueInput.value.replace(/\D+/g, ""));
	} else if (
		campoDeLetra.includes(props.tipoDeInput) &&
		typeof format[props.tipoDeInput] === "function"
	) {
		const maskedValue = format[props.tipoDeInput](event.target.value);
		valueInput.value = maskedValue;
		emits("inputEmitValue", valueInput.value);
	} else {
		emits("inputEmitValue", event.target.value);
	}
};

// const campoObrigatorio = computed(() => {
// 	if (props.obrigatorio && valueInput.value) return true;
// 	else return false;
// });

function unformatCurrency(value: string) {
	return value.replace(/[^0-9]/g, "");
}

function formatCurrency(value: any) {
	const number =
		typeof value === "string"
			? parseFloat(value.replace(/[^0-9.-]+/g, "")) / 100
			: value;

	/* Se for NaN, retorna uma string vazia */
	if (isNaN(number)) return "";

	/* Retorna o valor formatado como R$ n^X,XX
			Notação n^X: lê-se "n X", no sentido de "invariáveis quantidades de X"
		*/
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
};

onMounted(() => {
	if (props.valorPadrao) valueInput.value = props.valorPadrao;
	if (props.valor) {
		valueInput.value = props.valor;
		handleInput({ target: { value: valueInput.value } });
	}
});
</script>

<style scoped>

</style>