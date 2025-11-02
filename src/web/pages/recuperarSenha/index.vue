<template>
    <div v-if="step == 1" class="text-grayScale-800 flex flex-col gap-2">
        <div class="flex flex-col gap-1.5">
            <h1 class="text-2xl font-bold">Recuperação de senha</h1>
            <p class="text-grayScale-600">Informe seu email para continuar</p>
        </div>


        <div class="w-full">
            <Input tipoDeComponente="email" tipoDeInput="email" label="Email" propriedade="email" 
            :obrigatorio="true" :hasError="Boolean(erros['email'])" :errorMessage="erros['email']"
            @emiteValor="atualizarForm('email', $event)"
            />


            <div class="w-full mt-6">
                <button 
                class="bg-primary hover:opacity-80 duration-200 disabled:bg-grayScale-500 w-full rounded-md text-white h-12 shadow flex justify-center items-center" 
                @click="enviarCodigo">
                    <span v-if="true" class="text-primary-light font-semibold">Enviar código</span>
                    <Icon v-else nameIcon="ArrowPathIcon" class="text-white animate-spin"></Icon>
                </button>
            </div>
        </div>
    </div>


    <div v-if="step == 1" class="text-grayScale-800 flex flex-col gap-2">
        <div class="flex flex-col gap-1.5">
            <h1 class="text-2xl font-bold">Informe o código que enviamos via E-mail</h1>
            <p class="text-grayScale-600">Enviado para gbruno******@gmail.com</p>
        </div>


        <div class="w-full">
            <InputConfirmation  
                @complete="console.log('completo')"
            />


            <div class="w-full mt-6">
                <button 
                class="bg-primary hover:opacity-80 duration-200 disabled:bg-grayScale-500 w-full rounded-md text-white h-12 shadow flex justify-center items-center" 
                @click="enviarCodigo">
                    <span v-if="true" class="text-primary-light font-semibold">Verificar</span>
                    <Icon v-else nameIcon="ArrowPathIcon" class="text-white animate-spin"></Icon>
                </button>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { Campo } from "~/types/formulario";

    
const senhaVisivel = ref(false)

const senha = [
    {
        label: "Senha",
        propriedade: "password",
        obrigatorio: true,
        placeholder: "********"
    },
    {
        label: "Confirme a senha",
        propriedade: "confirmarSenha",
        obrigatorio: true,
        placeholder: "********"
    }
]


// const camposObrigatorios = computed(() => {
//     return formulario
//         .filter(campo => campo.obrigatorio)
//         .map(campo => campo.propriedade);
// });

// const camposOpcionais = computed(() => {
//     return formulario
//         .filter(campo => !campo.obrigatorio)
//         .map(campo => campo.propriedade);
// });

const { form, erros, formValido, validarCampo, validarFormulario } = useForm(['email'], ['senha', 'confirmarSenha']);

const atualizarForm = atualizarFormulario(form, validarCampo);

const step = ref(1)

async function enviarCodigo(){
    validarFormulario()

    if (!formValido.value) return

    step.value++


    // const { data, loading, error, execute } = useApi('post', '/login')
    // await execute({username: 'username', password: '1234'});
}

function novaSenha(){
    if (form.value.password !== form.value.confirmarSenha) {
    erros.value.confirmarSenha = "As senhas não coincidem"
    return
  }
}
</script>

<style scoped>

</style>