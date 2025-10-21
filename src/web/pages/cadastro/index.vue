<template lang="">
    <div>
        <p>Criar sua conta</p>
        <p>Informe seus dados para prosseguirmos!</p>
    </div>
    <div v-if="step==1">
        <Input v-for="(campo) in formularios" 
        :tipoDeComponente="campo.tipoDeInput"
        :tipoDeInput="campo.tipoDeInput"
        :model="campo.model"
        :modelType="campo.modelType"
        :label="campo.label"
        :validacao="campo.validacao"
        :obrigatorio="campo.obrigatorio"
        :placeholder="campo.placeholder"
        :hasError="Boolean(erros[campo.propriedade])"
        :errorMessage="erros[campo.propriedade]"
        @emiteValor="atualizarForm(campo.propriedade, $event, campo?.validacao)"
        />
        <div>
        <div></div>
        <button class="bg-primary" @click="nextStep">
            <span>Login</span>
        </button>
    </div>
</div>
</template>

<script setup lang="ts">

import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";


const formularios = [

            {
                label: "CPF",
                propriedade: "cpf",
                tipoDeInput: "cpf",
                validacao: "cpf",
                obrigatorio: true,
            },
            {
                label: "Nome",
                propriedade: "name",
                tipoDeInput: "nome",
                validacao: "nome",
                obrigatorio: true,
                placeholder: "Seu nome"
            },
            {
                label: "Data de nascimento",
                propriedade: "dt_birth",
                validacao: "data",
                tipoDeInput: "data",
                obrigatorio: true,
            },
            {
                label: "Celular",
                propriedade: "phone",
                tipoDeInput: "telefone",
                validacao: "telefone",
                obrigatorio: true,
            },
            {
        label: "E-mail",
        propriedade: "username",
        validacao: "email",
        tipoDeInput: "email",
        obrigatorio: true
    },
    {
                label: "Sexo",
                propriedade: "gender",
                tipoDeInput: "select",
                modelType: "static",
                model: [
                    {
                        chave: 'male',
                        descricao: "Masculino"
                    },
                    {
                    chave: 'female',
                        descricao: "Feminino"
                    },
                    {
                        chave: 'other',
                        descricao: "Outro"
                    },
                ],
            },
        ]

const { form, erros, formValido, validarCampo, validarFormulario } = useForm([ "name", "cpf" ],[]);

// Cria a função de atualização do formulário usando o helper componentizado
const atualizarForm = atualizarFormulario(form, validarCampo);

const step = ref(1)

function nextStep () {
    validarFormulario()
    if (!formValido.value) return
    step.value = 2
}

</script>

