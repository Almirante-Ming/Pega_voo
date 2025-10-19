<template>
	<div v-if="visivel" class="mb-5 border border-input-100 p-3 rounded-lg bg-grayScale-50 shadow-lg">
        <div class="flex justify-between items-center mb-3">
            <span v-if="props.label" for="default-input" class="font-medium text-grayScale-800">{{ props.label }}</span>
            <button
                @click="emit('removeimage')" 
                class="hover:ring-red-500 text-white text-sm ring-1 ring-grayScale-400 rounded-lg duration-150">
				<Icon
				:name-icon="'TrashIcon'"
				:class="'text-grayScale-500 duration-150 hover:text-red-500 w-7 h-7 px-1 py-1'"
				></Icon>
            </button>
        </div>

		<div class="flex w-full cursor-pointer rounded-lg hover:opacity-80 duration-200" @click="triggerFileInput" :class="{
				'cursor-not-allowed opacity-[0.55]': !habilitado,
				'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
				'ring-[0.0600rem] ring-primary': isInputFocused && !hasError,
			}">
			<div class="px-2 py-2 sm:min-w-[140px] rounded-l-lg bg-grayScale-300 text-grayScale-800 text-sm flex justify-center items-center text-center">Escolher arquivo</div>
			<div 
				
				class="flex items-center text-sm w-full border border-l-0 rounded-r-lg bg-input-100 border-input-200 text-grayScale-800 px-3 py-2 max-h-[60px] truncate"

			>
				<span class="max-w-full truncate">
					{{ previewUrl ? nomeArquivoSelecionado : (props.nome || 'Nenhum arquivo escolhido') }}
				</span>
			</div>

			<input
				ref="fileInputRef"
				type="file"
				class="hidden"
				:disabled="!habilitado"
				@change="handleFileChange"
			/>
		</div>

		<div v-if="loadingUpload" class="w-full mt-5 flex justify-center">
			<Icon
				:name-icon="'ArrowPathIcon'"
				:class="'text-grayScale-600 animate-spin'"
			></Icon>
		</div>
		<div v-if="!requesting" class="w-full pl-1 mt-1">
			<span class="text-[#ec6464] text-sm">{{ mensagemErro }}</span>
		</div>

        <div class="flex items-center justify-center flex-col">
            <div v-if="previewUrl && !requesting" class="mt-3 relative group flex items-center" style="height: 210px;">
                <img 
                    :src="previewUrl" 
                    alt="Pré-visualização" 
					style="max-height: 210px;"
                    class="rounded-lg opacity-100 group-hover:opacity-40 transition-opacity duration-300 ease-in-out" 
                />

                <button 
                    @click="emit('removeimage')" 
                    class="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 hover:bg-red-600 transition-all duration-300 ease-in-out">
                    Remover
                </button>
            </div>
            <div v-if="imageUrl && !previewUrl && !requesting" class="mt-3 relative group h-[210px]">

                <img 
                    :src="imageUrl" 
                    alt="Imagem da URL" 
                    class="h-full w-auto rounded-lg opacity-100 group-hover:opacity-40 transition-opacity duration-300" 
                />

                <!-- Botão de remover imagem que aparece ao passar o mouse -->
                <button 
                    @click="emit('removeimage')" 
                    class="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 hover:bg-red-600 transition-opacity duration-300 ease-in-out">
                    Remover
                </button>
            </div>
        </div>
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
		tag?: string;
		imageUrl?: string;
		tipoArquivo?: string;
	}

	const props = withDefaults(defineProps<Props>(), {
		tipoDeInput: String as PropType<Value>,
		habilitado: true,
		visivel: true,
		obrigatorio: false,
	});

	const fileInputRef = ref<HTMLInputElement | null>(null);

	const nomeArquivoSelecionado = ref('');

	function triggerFileInput() {
		fileInputRef.value?.click();
	}

	const imgCarregada = ref('')
	const selectedFile = ref({});
	const previewUrl = ref('');
	const mensagemErro = ref('');
	const requesting = ref(false)

	const { execute, error: errorUpload, data: dataArquivo, loading: loadingUpload } = useApi("post", `v2/builderGeneric?action=upload`);
	const emit = defineEmits(['inputEmitValue', 'removeimage'])


	async function handleFileChange(event: any) {
		const file = event.target.files[0];
		const storeDePraca = useStoreDePraca();
		const pracaId = computed(() => storeDePraca.getPracaId);
		const maxSize = 300 * 1024; 

		if (file) {
			if (file.size > maxSize ){ 
				mensagemErro.value = "O arquivo selecionado excede o limite de 300KB.";
				return;
			}
			requesting.value = true
			nomeArquivoSelecionado.value = file.name;

			const reader = new FileReader();
			reader.onload = (e: any) => {
				previewUrl.value = e.target.result;
			};
			reader.readAsDataURL(file);

			const formData = new FormData();
			if (pracaId.value) {
				formData.append('file', file);
				formData.append('tag', props.tag);
				formData.append('b2bFilter', pracaId.value.toString());
				formData.append('nome', props.tipoArquivo);
			}
			reader.onload = (e: any) => {
				imgCarregada.value = e.target.result;
			};

			await execute(formData);
			if (dataArquivo.value) {
				requesting.value = false
				mensagemErro.value = ''
				if (dataArquivo.value.arquivo_id) {
					selectedFile.value = file;
					emit('inputEmitValue', dataArquivo.value.arquivo_id);
					previewUrl.value = imgCarregada.value
				}else{
					mensagemErro.value = 'Ops, tente novamente por favor.';
					previewUrl.value = ''
				}
			} 
			if(errorUpload.value) {
				requesting.value = false
				mensagemErro.value = errorUpload.value ?? 'Ops, tente novamente por favor.';
				previewUrl.value = ''
			}
		} else {
			selectedFile.value = {};
			previewUrl.value = '';
		}
	}

	watch(() => props.errorMessage, (novoErro) => {		
		if (novoErro) {
			mensagemErro.value = novoErro;
		} else if (!mensagemErro.value) {
			mensagemErro.value = '';
		}
	});

	onBeforeMount(()=>{				
		emit('inputEmitValue', '');
	})
	const isInputFocused = ref(false);

	const handleInputFocus = () => {
		isInputFocused.value = true;
	};

	const handleInputBlur = () => {
		isInputFocused.value = false;
	};
</script>

<style scoped></style>
