<template>
	<div v-if="visivel" class="mb-5">
		<label v-if="props.label" for="default-input" class="mb-1 block font-medium text-grayScale-800">
			{{ props.label }}
		</label>
		<input @change="handleFileChange($event)" @focus="handleInputFocus" @blur="handleInputBlur" type="file"
			:nome="props.nome" :placeholder="placeholder" :disabled="!habilitado" autocomplete="off" :class="clsx({
				'cursor-not-allowed opacity-[0.55]': !habilitado,
				'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
				'ring-[0.0600rem] ring-primary': isInputFocused && !hasError,
			},
				'block w-full text-sm border rounded-lg cursor-pointer bg-input-100 border-input-200'
			)
				" />
		<span class="text-[#ff3b3b] text-sm">{{ errorMessagem }}</span>
	</div>
</template>

<script setup lang="ts">
import clsx from "clsx";

interface Props {
	label?: string;
	tipoDeInput?: any; //cpf, data,
	tipoDeDado?: string; //input, select
	placeholder?: string;
	obrigatorio?: boolean;
	visivel?: boolean;
	hasSuccess?: boolean;
	hasError?: boolean;
	errorMessage?: string;
	habilitado?: boolean;
	propriedade?: string;
	valor?: any;
	nome: String;
	b2b: number;
	tag?: string
}

const props = withDefaults(defineProps<Props>(), {
	tipoDeInput: String as PropType<Value>,
	habilitado: true,
	visivel: true,
	obrigatorio: false,
});

const selectedFile = ref({});
const previewUrl = ref('');
const errorMessagem = ref('');

const { execute, error: errorUpload, data: dataArquivo, loading: loadingUpload } = useApi("post", `v2/builderGeneric?action=upload`);
const emit = defineEmits(['inputEmitValue'])

async function handleFileChange(event: any) {
	const file = event.target.files[0];  // Obtem o primeiro arquivo, se houver
	const storeDePraca = useStoreDePraca();
	const pracaId = computed(() => storeDePraca.getPracaId);

	if (file) {
		const formData = new FormData()

		if (pracaId.value) {
			formData.append('file', file);
			formData.append('tag', props.tag);
			formData.append('b2bFilter', pracaId.value.toString());
			formData.append('nome', props.propriedade);
		}

		await execute(formData);

		if (!errorUpload.value && dataArquivo.value) {
			if (dataArquivo.value.success) {
				selectedFile.value = file;
				const reader = new FileReader();
				reader.onload = (e: any) => {
					previewUrl.value = e.target.result;  // Atualiza a URL de pré-visualização
				};
				reader.readAsDataURL(file)
				emit('inputEmitValue', dataArquivo.value.arquivo_id);
				errorMessagem.value = '';
			}
		} else {
			errorMessagem.value = errorUpload.value;
		}
	} else {
		selectedFile.value = {};
		previewUrl.value = '';
	}
}


const isInputFocused = ref(false);

const handleInputFocus = () => {
	isInputFocused.value = true;
};

const handleInputBlur = () => {
	isInputFocused.value = false;
};
</script>

<style scoped></style>