<template>
	<div v-if="visivel" class="mb-5">
		<label
			v-if="props.label"
			for="default-input"
			class="mb-1 block font-medium text-grayScale-800"
			>{{ props.label }}
		</label>
		<input
			v-model="valueInput"
			@input="handleInput($event)"
			@keydown="handleInput($event)"
			@focusout="handleInput($event)"
			@focus="handleInputFocus"
			@blur="handleInputBlur"
			@keydown.enter.prevent="$event.preventDefault()"
			type="text"
			:valorPadrao="props.valorPadrao"
			placeholder="dd/mm/aaaa"
			:disabled="!habilitado"
			autocomplete="off"
			:class="
				clsx(
					'block w-full rounded-lg p-2.5 text-sm custom-number-input text-grayScale-800 placeholder:text-grayScale-450 bg-input-100 border border-input-200 focus:border-primary focus:ring-primary focus:outline-none',
					{
						'cursor-not-allowed opacity-[0.55]': !habilitado,
						'ring-[0.0600rem] ring-[#ff3b3b]': props.hasError && !hasSuccess || hasErrors && !hasSuccess,
						'ring-[0.0600rem] ring-primary': isInputFocused && !hasError,
						// 'ring-[0.0600rem] ring-[#22bb33]':
						// 	!hasError && hasSuccess && valueInput,
					}
				)
			"
		/>
		<span v-if="props.errorMessage" class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
	</div>
</template>

<script setup lang="ts">
import clsx from "clsx";
import { format } from "@/utils";

interface Props {
	label?: string;
	tipoDeDado?: string; //input, select
	valorPadrao?: any;
	placeholder?: string;
	obrigatorio?: boolean;
	visivel?: boolean;
	habilitado?: boolean;
	propriedade?: string;
	valor?:any
	hasError:boolean;
	errorMessage:string;
}

const props = withDefaults(defineProps<Props>(), {
	tipoDeDado: "string", //string, number, boolean
	habilitado: true,
	visivel: true,
	obrigatorio: false
});

const emits = defineEmits(["inputEmitValue"]);

const valueInput = ref();

const hasErrors = ref();

const hasSuccess = ref(false);

const handleInput = (event: any) => {
	
	if(valueInput.value == '' && !props.obrigatorio){
		hasErrors.value = false
		emits("inputEmitValue", '');

	}else{		
		const maskedValue = format["data"](event.target.value);
		valueInput.value = maskedValue
		emits('inputEmitValue', formatDate(maskedValue))			
	}
};

function formatDate(dateStr) {
    const [day, month, year] = dateStr.split('/');
    return `${year}-${month}-${day}`;
}

function formatToDisplayFormat(dateStr: string): string {
    if (!dateStr) return '';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
}

const isInputFocused = ref(false);

const handleInputFocus = () => {
	isInputFocused.value = true;
};

const handleInputBlur = () => {
	isInputFocused.value = false;
};

onMounted(() => {
    if (props.valorPadrao) {
        const formattedValue = formatToDisplayFormat(props.valorPadrao);
        valueInput.value = formattedValue;
        handleInput({ target: { value: formattedValue } });
    }
    if (props.valor) {
        const formattedValue = formatToDisplayFormat(props.valor);
        valueInput.value = formattedValue;
        handleInput({ target: { value: formattedValue } });
    }
});

</script>

<style scoped></style>
