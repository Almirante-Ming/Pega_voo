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
                :label="campo.label"
                :propriedade="campo.propriedade"
                :model="campo.model"
                :modelType="campo.modelType"
                :obrigatorio="campo.obrigatorio"
                :placeholder="campo.placeholder"
                :tipoDeDado="campo.tipoDeDado"
                :valoresNegativos="campo.valoresNegativos"
                :hasError="Boolean(erros[campo.propriedade])"
                :errorMessage="erros[campo.propriedade]"
                :mostrarHora="campo.mostrarHora"
                @emiteValor="atualizarForm(campo.propriedade, $event, campo?.validacao)"
            />
        </div>
    </div>
    <div class="bg-primary text-grayScale-50 p-3 rounded-md">
        <p>Estado do formulário:</p>
        {{ form }}
    </div>
    <div class="w-full mt-3">
        <button :disabled="loading" class="bg-green-600 disabled:bg-grayScale-500 w-full rounded-md text-grayScale-50 h-10 shadow flex justify-center items-center" @click="login">
            <span v-if="!loading">Login</span>
            <Icon v-else nameIcon="ArrowPathIcon" class="text-grayScale-50 animate-spin"></Icon>
        </button>
    </div>
</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { Formulario } from "~/types/formulario";

const { data, loading, error, execute } = useApi('post', '/login', { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })

// Se não for formData
// const { data, loading, error, execute } = useApi('post', '/login')
// await execute({username: 'username', password: '1234'});

async function login(){
    const params = new URLSearchParams();
    params.append('username', 'user@email.com');
    params.append('password', 'pas');

    await execute(params.toString());
}

const formulario: Formulario = [
    {
        title: "Perguntas Importantes",
        columns: [
            {
                label: "Tudo bem com você?",
                tipoDeDado: "string",
                propriedade: "tudoBem",
                tipoDeInput: "select",
                obrigatorio: true,
                modelType: "static" as const,
                placeholder: "Escolha uma opção",
                model: [
                    { chave: "sim", descricao: "Sim" },
                    { chave: "nao", descricao: "Não" },
                    { chave: "claro", descricao: "Claro que sim" }
                ]
            }
        ]
    },
    {
        title: "Informações Pessoais",
        columns: [
            {
                label: "CPF",
                propriedade: "cpfCliente",
                tipoDeInput: "cpf",
                validacao: "cpf",
                obrigatorio: true,
                placeholder: "000.000.000-00"
            },
            {
                label: "Sexo",
                propriedade: "sexo",
                tipoDeInput: "select",
                modelType: "static",
                model: [
                    {
                        chave: 'M',
                        descricao: "Masculino"
                    },
                    {
                    chave: 'F',
                        descricao: "Feminino"
                    },
                    {
                        chave: 'O',
                        descricao: "Outro"
                    },
                ],
            },
            {
                label: "Celular",
                tipoDeDado: "string",
                propriedade: "telefoneUsuario",
                tipoDeInput: "telefone",
                validacao: "telefone",
                obrigatorio: true,
                placeholder: "(00) 00000-0000"
            }
        ]
    },
        {
        title: "Campos não obrigatórios",
        columns: [
            {
                label: "Data de nascimento",
                propriedade: "dataNascimento",
                validacao: "data",
                tipoDeInput: "data",
                obrigatorio: false,
            },
            {
                label: "Data de hoje",
                propriedade: "dataAtual",
                tipoDeInput: "timestamp",
                validacao: "data",
                obrigatorio: false,
                mostrarHora: false
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

const { form, erros, formValido, validarCampo, validarFormulario } = useForm(camposObrigatorios.value, camposOpcionais.value);

// Cria a função de atualização do formulário usando o helper componentizado
const atualizarForm = atualizarFormulario(form, validarCampo);


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