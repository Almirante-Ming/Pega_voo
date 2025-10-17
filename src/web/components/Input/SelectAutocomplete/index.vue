<template>
	<div v-if="visivel && props.modelType == 'dynamic'" class="w-full" :class="clsx({ 'mb-4': props.marginBottom })">
		<label v-if="props.label" for="default-input" class="mb-1 block font-medium text-grayScale-800">{{ props.label
		}}
		</label>
		<div class="flex flex-col w-full relative">
			<input v-model="content" @input="results" @focus="handleInputFocus" @focusout="resetContent"
				@keydown.enter.prevent="$event.preventDefault()" @blur="handleInputBlur" :maxlength="props.maxLength"
				type="text" :placeholder="'Buscar...'" :disabled="!habilitado" autocomplete="off" :class="clsx(
					'block w-full rounded-lg bg-input-100 border border-input-200 p-2.5 text-sm focus:border-primary focus:ring-primary focus:outline-none outline-none shadow-none text-grayScale-800 ',
					{
						'cursor-not-allowed opacity-[0.55]': !habilitado,
						'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
						'ring-[0.0600rem] ring-primary rounded-b-none': isOpen,
						'ring-[0.0600rem] ring-[#22bb33]':
							!hasError && hasSuccess && content,
					}
				)
			"/>
			<ul v-if="isOpen && filteredResults?.length > 0"
				:class="`absolute w-full top-[43px] rounded-t-lg overflow-x-hidden z-[999] max-h-[180px] overflow-y-auto rounded-b-lg bg-input-100 border border-input-200 ${animation}  ease-in-out`">
				<li v-for="(opcao, index) in filteredResults" :class="clsx({
					'hover:rounded-b-lg': index === filteredResults.length - 1,
				})
					" class="cursor-pointer border-b border-input-200 py-2 hover:brightness-110 hover:bg-grayScale-300 flex " @mousedown="selectContent(opcao)">
					<span v-if="opcao && opcao.descricao" class="w-full flex-wrap text-sm ml-2 text-grayScale-800 ">
						{{ opcao.descricao }}
					</span>
				</li>
			</ul>
		</div>
		<span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
	</div>

	<div v-if="visivel && props.modelType == 'static'" class="w-full cursor-pointer relative"
		:class="clsx({ 'mb-4': props.marginBottom })">
		<label v-if="props.label" for="default-input" class="mb-1 block font-medium text-grayScale-800">{{ props.label
		}}
		</label>
		<div @click="showOptions()" class="" @focus="handleInputFocus" @blur="handleInputBlur" :class="clsx(
			'w-full flex items-center rounded-lg bg-input-100 border border-input-200 p-2.5 text-sm focus:outline-none text-grayScale-800 outline-none shadow-none h-[42px] gap-2',
			{
				'cursor-not-allowed opacity-[0.55]': !habilitado,
				'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
				'ring-[0.0600rem] ring-primary border-primary': isOpen,
				'ring-[0.0600rem] ring-[#22bb33]':
					!hasError && hasSuccess && content,
			}
		)
			">
			<div class="w-[98%] flex-nowrap truncate">
				<span v-if="!selectedOption" class="text-grayScale-600">Selecione uma opção</span>
				<div class="flex items-center gap-1.5" v-else>
					<span class="max-w-[90%] truncate">{{ selectedOption?.descricao }}</span>
					<DesignV2IconHero v-if="excluirItem" @click.stop="removeSelectedOption" name-icon="XCircleIcon"
						class="text-grayScale-700 hover:text-red-400 duration-150 w-6 h-6" />
				</div>
			</div>
			<div>
				<DesignV2IconHero name-icon="ChevronDownIcon" class="text-grayScale-700 duration-150"
					:class="clsx({ 'rotate-180': isOpen })" />
			</div>
		</div>
		<ul v-if="isOpen"
			:class="`absolute mt-[1px] rounded-t-lg w-full z-[999] max-h-[195px] overflow-y-auto rounded-b-lg bg-input-100 border border-input-200 ${animation} ease-in-out`">
			<li v-for="(opcao, index) in completeList" :class="clsx('hover:brightness-110 hover:bg-grayScale-300', {
				'bg-grayScale-300': (opcao?.chave != null && opcao?.chave == selectedOption?.chave) || (opcao?.id != null && opcao?.id == selectedOption?.id)
			})
				" class="cursor-pointer border-b border-input-200 px-4 py-[9px] flex flex-col last:border-b-0 duration-150"
				@mousedown="selectContent(opcao)">
				<span v-if="opcao && opcao.descricao" class="text-grayScale-800 text-sm">
					{{ opcao.descricao }}
				</span>
				<span v-if="opcao && opcao.labelExplicativa" class="text-grayScale-600 text-xs xl:!text-sm">
					({{ opcao.labelExplicativa }})
				</span>
			</li>
			<li v-if="!completeList?.length" class="border-b border-input-200 px-4 py-2 flex justify-center">
				<span class="text-center">
					Sem resultados
				</span>
			</li>

		</ul>
		<span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
	</div>
</template>

<script setup lang="ts">
import type { InputHTMLAttributes } from "vue";

import { clsx } from "clsx";


enum Placeholders {
	AUTOCOMPLETE = "Pesquisar",
	SELECT = "Selecionar",
}

type PlaceholderKeys = keyof typeof Placeholders;

interface InputSelectAutocompleteProps {
	label?: string;
	hasSuccess?: boolean;
	hasError?: boolean;
	errorMessage?: string;
	habilitado?: boolean;
	type?: InputHTMLAttributes["type"];
	placeholder?: InputHTMLAttributes["placeholder"];
	placeholderType?: PlaceholderKeys;
	value?: string;
	valorPadrao?: any;
	inputType: string;
	maxLength?: number;
	model?: any[];
	modelType?: "static" | "dynamic";
	visivel?: boolean;
	propriedade: any;
	informacoesAction?: any;
	valor?: any;
	obrigatorio?: boolean;
	tipoDeDado?: string;
	marginBottom?: boolean;
	excluirItem?: boolean
}

const props = withDefaults(defineProps<InputSelectAutocompleteProps>(), {
	habilitado: true,
	visivel: true,
	obrigatorio: false,
	marginBottom: true,
	excluirItem: false
});

const completeList = computed(() => props.model);
const inputType = ref(props.inputType);

const emit = defineEmits(["emitValue"]);
const content = defineModel();
defineExpose({ focus });

const inputRef = ref();
const selectedOption = ref();
const isOpen = ref(false);
const isInputFocused = ref(false);
const resultNotFound = ref(false);
const animation = ref("opening");

const selecionaPlaceholder = () => {
	if (props.placeholderType) {
		return Placeholders[props.placeholderType];
	}
	return props.placeholder;
};

function focus() {
	inputRef.value?.focus();
}

const handleInputFocus = () => {
	isInputFocused.value = true;
	if (
		!isOpen.value &&
		props.modelType == "dynamic" &&
		!valorSelecionado.value &&
		content.value
	)
		showOptions();
};

const handleInputBlur = () => {
	isInputFocused.value = false;
	closeOptions();
};

const filteredResults = computed(() => props.model || []);
const parouDeDigitar = ref(false);
//@ts-ignore
let timeoutId;

async function results() {
	valorSelecionado.value = false;
	parouDeDigitar.value = false;
	resultNotFound.value = false;

	if (timeoutId) {
		clearTimeout(timeoutId);
	}

	timeoutId = setTimeout(async () => {
		parouDeDigitar.value = true;
		if (content.value) {
			emit("emitValue", content.value);
			showOptions();
		} else {
			closeOptions();
		}
	}, 350);
}

const valorSelecionado = ref();

function selectContent(item: any) {
	if (inputType.value == "select" && props.modelType == "dynamic") {
		content.value = item.descricao;
		emit("emitValue", item);
		closeOptions();
		valorSelecionado.value = true;
	} else if (item.chave && item.chave != selectedOption.value?.chave) {
		selectedOption.value = item;
		emit("emitValue", selectedOption.value);
		closeOptions();
	} else {
		selectedOption.value = item;
		emit("emitValue", selectedOption.value);
		closeOptions();
	}
}

function removeSelectedOption() {
	selectedOption.value = undefined;
	emit("emitValue", undefined);
}

//como o select é uma div e não possui a propriedade de focus para controlar o fechamento dele ao clicar fora dele, devemos usar esse event listener
window.addEventListener("mouseup", function (e: any) {
	if (isOpen.value == true && inputType.value == "select") {
		if (
			!document.getElementById("selectBox")?.contains(e?.target) &&
			props.modelType == "static"
		) {
			closeOptions();
		}
	}
});

function closeOptions() {
	animation.value = "closing";
	setTimeout(() => {
		isOpen.value = false;
		animation.value = "opening";
	}, 75);
}

function showOptions() {
	if (isOpen.value == false) {
		isOpen.value = true;
	}
}

function resetContent() {
	if (!valorSelecionado.value) {
		content.value = "";
		emit("emitValue", "");
		valorSelecionado.value = false;
		parouDeDigitar.value = false;
		resultNotFound.value = false;
	}
}

onMounted(() => {
	if (props.valor && props.modelType == 'dynamic') {
		content.value = props.valor.descricao
		valorSelecionado.value = true
		emit("emitValue", props.valor?.chave)
	}
	
	else if (props.valorPadrao && props.modelType == 'static'  && props.valorPadrao.hasOwnProperty('id')) {
		selectedOption.value = props.valorPadrao;		
	}
	else if (props.valor !== null && props.valor !== undefined && props.valor !== '' && props.modelType === 'static') {
		emit("emitValue", props.valor)

		props.model?.forEach(select => {
			if (props.valor == select.chave) {
				selectedOption.value = select
			}
		})
	}
	else if (props.valorPadrao && props.modelType == 'static') {
		emit("emitValue", props.valorPadrao)

		props.model?.forEach(select => {
			if (props.valorPadrao == select.chave) {
				selectedOption.value = select
			}
		})	
	} 
});
</script>

<style scoped>
@keyframes closing {
	0% {
		opacity: 100%;
	}

	100% {
		opacity: 0%;
	}
}

@keyframes opening {
	0% {
		opacity: 0%;
	}

	100% {
		opacity: 100%;
	}
}

.closing {
	animation: closing 0.15s forwards;
}

.opening {
	animation: opening 0.15s forwards;
}
</style>