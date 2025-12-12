<template>
	<div :class="clsx('w-full', {
		'flex items-center': props?.itemsCenter
	})">
		<InputData v-if="nomesData.includes(props.tipoDeComponente)" @inputEmitValue="emitValue"
			@emiteKeydown="emitValue" @emiteFocusout="emitValue" :valor="props.valorVmodel"
			:propriedade="props.propriedade" :label="props.label" :obrigatorio="props.obrigatorio"
			:valorPadrao="props.valorPadrao" :tipoDeDado="props.tipoDeDado" :visivel="props.visivel"
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" />

		<InputDatePicker v-else-if="
			props.tipoDeComponente == 'dataHora' || props.tipoDeComponente == 'timestamp'
		" @inputEmitValue="emitValue" @emiteKeydown="emitValue" @emiteFocusout="emitValue" :valor="props.valorVmodel"
			:propriedade="props.propriedade" :label="props.label" :obrigatorio="props.obrigatorio"
			:valorPadrao="props.valorPadrao" :tipoDeDado="props.tipoDeDado" :visivel="props.visivel"
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" :mostrarHora="props.mostrarHora"/>

		<InputCheckboxUnica v-else-if="props.tipoDeComponente == 'checkbox'"
			@inputEmitValue="emitValue" :propriedade="props.propriedade" :valor="props.valorVmodel" :label="props.label"
			:obrigatorio="props.obrigatorio" :tipoDeInput="props.tipoDeInput" :valorPadrao="props.valorPadrao" :marginBottom="props.marginBottom"
			:model="props.model" :tipoDeDado="props.tipoDeDado" :visivel="props.visivel"
			:errorMessage="props.errorMessage" :habilitado="props.habilitado" />

		<InputRadio v-else-if="props.tipoDeComponente == 'radioButton'" @inputEmitValue="emitValue"
			:propriedade="props.propriedade" :valor="props.valorVmodel" :label="props.label"
			:obrigatorio="props.obrigatorio" :valorPadrao="props.valorPadrao" :model="props.model"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" />

		<InputSelectAutocomplete v-else-if="props.tipoDeComponente == 'select'" @emitValue="emitValue"
			:valor="props.valorVmodel" :label="props.label" :obrigatorio="props.obrigatorio" :marginBottom="props.marginBottom"
			:inputType="props.tipoDeInput" :modelType="props.modelType" :valorPadrao="props.valorPadrao" :excluirItem="props.excluirItem"
			:model="props.model" :tipoDeDado="props.tipoDeDado" :maxLength="props.maxLength" :visivel="props.visivel"
			:placeholder="props.placeholder" :hasSuccess="props.hasSuccess" :hasError="props.hasError"
			:errorMessage="props.errorMessage" :habilitado="props.habilitado" :propriedade="props.propriedade"
			:informacoesAction="informacoesAction" />

		<InputLista v-else-if="props.tipoDeComponente == 'list'"  @emitValue="emitValue" @emitSelected="emitSelectedOption"
			:valor="props.valorVmodel" :label="props.label" :obrigatorio="props.obrigatorio" :marginBottom="props.marginBottom"
			:inputType="props.tipoDeInput" :modelType="props.modelType" :valorPadrao="props.valorPadrao"
			:model="props.model" :tipoDeDado="props.tipoDeDado" :maxLength="props.maxLength" :visivel="props.visivel"
			:placeholder="props.placeholder" :hasSuccess="props.hasSuccess" :hasError="props.hasError"
			:errorMessage="props.errorMessage" :habilitado="props.habilitado" :propriedade="props.propriedade"
			:informacoesAction="informacoesAction" :automatico="props?.automatico" />


		<InputIcon v-else-if="props.icone" @inputEmitValue="emitValue" @emiteKeydown="emitValue"
			@emiteFocusout="emitValue" @emitClick="emitClick" :valor="props.valorVmodel"
			:propriedade="props.propriedade" :label="props.label" :obrigatorio="props.obrigatorio"
			:maxLength="props.maxLength" :valorPadrao="props.valorPadrao" :tipoDeInput="props.tipoDeInput"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :placeholder="props.placeholder"
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" :icone="props?.icone" :marginBottom="props.marginBottom">
		</InputIcon>

		<InputUpload v-else-if="props.tipoDeComponente == 'fileUpload'" @inputEmitValue="emitValue"
			@emitClick="emitClick" :valor="props.valorVmodel" :propriedade="props.propriedade" :tag="props.tag"
			:label="props.label" :obrigatorio="props.obrigatorio" :tipoDeInput="props.tipoDeInput"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :placeholder="props.placeholder"
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" :icone="props?.icone" :nome="props?.nome">
		</InputUpload>

		<InputUploadPreview v-else-if="props.tipoDeComponente == 'fileUploadPreview'" @inputEmitValue="emitValue"
			@emitClick="emitClick" @removeimage="emits('emitRemoveImage')" :valor="props.valorVmodel" :propriedade="props.propriedade" :tag="props.tag"
			:label="props.label" :obrigatorio="props.obrigatorio" :tipoDeInput="props.tipoDeInput"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :placeholder="props.placeholder"
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" :icone="props?.icone" :nome="props?.nome" :imageUrl="props?.imageUrl" :tipoArquivo="props.tipoArquivo">
		</InputUploadPreview>

		<InputTextArea v-else-if="props.tipoDeComponente == 'textArea'" @inputEmitValue="emitValue"
			@emiteKeydown="emitValue" @emiteFocusout="emitValue" :valor="props.valorVmodel" :valoresNegativos="props.valoresNegativos"
			:propriedade="props.propriedade" :label="props.label" :obrigatorio="props.obrigatorio"
			:maxLength="props.maxLength" :valorPadrao="props.valorPadrao" :tipoDeInput="props.tipoDeInput"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :placeholder="props.placeholder" 
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado">
		</InputTextArea>

		<InputBaseInput v-else-if="props.tipoDeComponente" @inputEmitValue="emitValue"
			@emiteKeydown="emitValue" @emiteFocusout="emitValue" :valor="props.valorVmodel" :valoresNegativos="props.valoresNegativos"
			:propriedade="props.propriedade" :label="props.label" :obrigatorio="props.obrigatorio"
			:maxLength="props.maxLength" :valorPadrao="props.valorPadrao" :tipoDeInput="props.tipoDeInput"
			:tipoDeDado="props.tipoDeDado" :visivel="props.visivel" :placeholder="props.placeholder" 
			:hasSuccess="props.hasSuccess" :hasError="props.hasError" :errorMessage="props.errorMessage"
			:habilitado="props.habilitado" :tresCasasDecimais="props.tresCasasDecimais" :marginBottom="props.marginBottom">
		</InputBaseInput>
	</div>
</template>

<script setup lang="ts">
import clsx from "clsx";
const emits = defineEmits(["emiteValor", "emitClick", "emitRemoveImage", "emitSelected"]);
const nomesData = ['data', 'date', 'dateOfBirth', 'dataNasc', 'dataDeNascimento', 'dataNascimento', 'data_nascimento', 'data_de_nascimento', 'calendar']

function emitValue(value: any) {
	emits("emiteValor", value);
}
function emitSelectedOption(value: any) {
	emits("emitSelected", value);
}

function emitClick(value: any) {
	emits("emitClick", value);
}

interface Props {
	label?: string;
	tipoDeInput: any; // cpf, data, fileUpload, email, senha
	tipoDeDado?: string; // string, number, boolean
	valorPadrao?: any;
	placeholder?: string; // para select. AutoComplete falta desenvolver
	obrigatorio?: boolean; // Usado pelo useForm
	maxLength?: number;
	visivel?: boolean;
	hasSuccess?: boolean;
	hasError?: boolean;
	errorMessage?: string;
	habilitado?: boolean;
	propriedade?: string; // nome que a API espera, é para payload
	tipoDeComponente: string; // é o mesmo que o tipo de input e ele renderiza um inputType HTML baseado nessa variável
	model?: any; // lista estática chave e valor
	modelType?: "static" | "dynamic" | "static-list" | "dynamic-list"; // essa propriedade está diretamente relacionada com o model
	firstOption?: any; // serve para renderizar a opção selecionada no select
	query?: string; // Não está implementada. Vem da response quando modelType = 'dynamic'
	valorVmodel?: any;
	icone?: any;
	informacoesAction?: any;
	nome?: string;
	tag?: string;
	valoresNegativos?: boolean;
	itemsCenter?: boolean;
	imageUrl?: string;
	tipoArquivo?: string;
	marginBottom?: boolean;
	tamanhoMaximo?: number;
	automatico?: boolean;
	mostrarHora?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
	habilitado: true,
	visivel: true,
	marginBottom: true
});
</script>

<style scoped></style>