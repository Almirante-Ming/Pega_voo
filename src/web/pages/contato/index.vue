<template>
    <div>
        <div v-for="(grupo, index) in formulario" :key="index" class="mb-6">
            <h2 v-if="grupo.title" class="text-xl font-semibold mb-4 text-grayScale-800">
                {{ grupo.title }}
            </h2>
            <Input 
                v-for="campo in grupo.columns"
                :key="campo.propriedade"
                :tipoDeComponente="campo.tipoDeInput"
                :tipoDeInput="campo.tipoDeInput"
                :validation="campo.validation"
                :label="campo.label"
                :propriedade="campo.propriedade"
                :model="campo.model"
                :modelType="campo.modelType"
                :obrigatorio="campo.obrigatorio"
                :placeholder="campo.placeholder"
                :tipoDeDado="campo.tipoDeDado"
                :valoresNegativos="campo.valoresNegativos"
                :errorMessage="errors[campo.propriedade]"
                @emiteValor="atualizarFormulario(campo.propriedade, $event)"
            />
        </div>
    </div>
    <div class="bg-primary-light text-white p-3 rounded-md">
        <p>Estado do formulário:</p>
        {{ form }}
    </div>
</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import type { Formulario, GrupoFormulario } from "~/types/formulario";

const formulario: Formulario = [
    {
        title: "Perguntas Importantes",
        columns: [
            {
                label: "Namora comigo?",
                tipoDeDado: "string",
                propriedade: "namoraComigo",
                tipoDeInput: "select",
                obrigatorio: true,
                modelType: "static" as const,
                placeholder: "Escolha uma opção",
                model: [
                    { chave: "sim", descricao: "Sim" },
                    { chave: "nao", descricao: "Não" },
                    { chave: "talvez", descricao: "Talvez" }
                ]
            }
        ]
    },
    {
        title: "Informações Pessoais",
        columns: [
            {
                label: "CPF",
                tipoDeDado: "string",
                propriedade: "cpf",
                tipoDeInput: "string",
                validation: "cpf",
                obrigatorio: true,
                placeholder: "000.000.000-00"
            },
            {
                label: "Celular",
                tipoDeDado: "string",
                propriedade: "phone",
                tipoDeInput: "string",
                validation: "telefone",
                obrigatorio: true,
                placeholder: "(00) 00000-0000"
            }
        ]
    }
];

const camposObrigatorios = computed(() => {
    return formulario
        .flatMap(campoGrupo => campoGrupo.columns)
        .filter(campo => campo.obrigatorio)
        .map(campo => campo.propriedade);
});

const camposOpcionais = computed(() => {
    return formulario
        .flatMap(campoGrupo => campoGrupo.columns)
        .filter(campo => !campo.obrigatorio)
        .map(campo => campo.propriedade);
});

const { form, errors, formIsValid, handleValidateField, handleValidateFields } = useForm(camposObrigatorios.value, camposOpcionais.value);


function atualizarFormulario(field: string, value: any){
    form.value[field] = value?.target?.value
        ? value.target.value
        : typeof value === "boolean"
        ? value
        : typeof value === "string" || typeof value === "number"
        ? value
        : value?.chave ?? ""
    
    handleValidateField(field);
}





// Caso o formulario seja de edição (precisa receber os valores ao abrir a página ou componente)

// const dadosDeEdicao = {
//     cpf: "016.475.091-65",
//     telefone: "67984727983",
//     dataDeNascimento: "2001-03-02"
// }

// onMounted(()=>{
//     if (dadosDeEdicao) {
//         const formEdicao = dadosDeEdicao;
//         const formTransformado = Object.fromEntries(
//             Object.entries(formEdicao)
//                 .filter(([key, value]) => camposObrigatorios.value.includes(key) || camposOpcionais.value.includes(key))
//         );

//         form.value = { ...formTransformado };
//     }
// })
</script>

<style scoped>

</style>