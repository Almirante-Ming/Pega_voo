<template>
    <button @click="voltar" class="flex w-fit pr-4 py-1.5">
        <Icon nameIcon="ChevronLeftIcon"></Icon>
        Voltar
    </button>
    <div class="text-grayScale-800 flex flex-col gap-4">

        <div class="flex flex-col gap-1.5">
            <h1 class="text-2xl font-bold">{{stepInfo.titulo}}</h1>
            <p class="text-grayScale-600">{{stepInfo.subtitulo}}</p>
        </div>


        <div class="w-full">
            <div v-if="step == 1">
                <Input tipoDeComponente="email" tipoDeInput="email" label="Email" propriedade="email" 
                :obrigatorio="true" :hasError="Boolean(erros['email'])" :errorMessage="erros['email']"
                @emiteValor="atualizarForm('email', $event)"
                />
            </div>


            <div v-else-if="step == 2" class="w-full flex flex-col gap-2">
                <InputConfirmation  
                    @complete="console.log('completo')"
                />
            
                <span class="text-sm">
                    Não recebeu o código? 
                    <button v-if="true" class="text-primary underline px-1">Reenviar</button>
                    <span v-else class="text-grayScale-400">Aguarde: 2min 38seg</span>
                </span>
            </div>


            <div v-else-if="step == 3">
                <Input
                    v-for="(campo, index) in senha"
                    :tipoDeComponente="senhaVisivel ? 'string' : 'senha'"
                    :tipoDeInput="senhaVisivel ? 'string' : 'senha'" 
                    :label="campo.label"
                    :propriedade="campo.propriedade" 
                    :hasError="Boolean(erros[campo.propriedade])"
                    :errorMessage="erros[campo.propriedade]"
                    :icone="senhaVisivel ? 'EyeIcon' : 'EyeSlashIcon'"
                    :placeholder="campo.placeholder"
                    @emitClick="senhaVisivel = !senhaVisivel"
                    @emiteValor="atualizarForm(campo.propriedade, $event, '')"
                />
            </div>
        </div>



        <div class="w-full">
            <button 
            class="bg-primary hover:opacity-80 duration-200 disabled:bg-grayScale-500 w-full rounded-md text-white h-12 shadow flex justify-center items-center" 
            @click="enviarCodigo">
                <span v-if="true" class="text-primary-light font-semibold">{{stepInfo.textoBotao}}</span>
                <Icon v-else nameIcon="ArrowPathIcon" class="text-white animate-spin"></Icon>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { Campo } from "~/types/formulario";

const router = useRouter();

const step = ref(1)

const stepInfo = computed(() => {
    const steps = {
        1: {
            titulo: "Recuperação de senha",
            subtitulo: "Informe seu email para continuar",
            textoBotao: "Enviar código"
        },
        2: {
            titulo: "Informe o código que enviamos via E-mail",
            subtitulo: `Enviado para ${form.value.email}`,
            textoBotao: "Verificar"
        },
        3: {
            titulo: "Digite sua nova senha",
            subtitulo: "Agora escolha sua nova senha para continuar.",
            textoBotao: "Confirmar"
        }
    }
    return steps[step.value as keyof typeof steps]
})

    
const senhaVisivel = ref(false)

const senha = [
    {
        label: "Nova senha",
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


const { form, erros, formValido, validarCampo, validarFormulario } = useForm(['email'], ['senha', 'confirmarSenha']);

const atualizarForm = atualizarFormulario(form, validarCampo);

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

function voltar(){
    if(step.value == 1){
        router.go(-1)
    } else{
        step.value--
    }
}
</script>

<style scoped>

</style>