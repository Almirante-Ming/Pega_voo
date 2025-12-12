<template>
    <div class="text-grayScale-800 flex flex-col gap-4 mt-2">
        <Stepper 
            :steps="stepperSteps"
            :currentStep="step"
        />

        <div class="flex flex-col gap-1.5">
            <div class="flex items-center gap-2">
                <BackButton :action="voltar" />
                <h1 class="text-2xl font-bold">{{stepInfo.titulo}}</h1>
            </div>
            <p class="text-grayScale-600">{{stepInfo.subtitulo}}</p>
        </div>


        <div class="w-full">
            
            <div v-if="step == 1">
                <Input tipoDeComponente="email" tipoDeInput="email" label="Email" propriedade="email" 
                :obrigatorio="true" :hasError="Boolean(erros['email'])" :errorMessage="erros['email']"
                @emiteValor="atualizarForm('email', $event)"
                />
            </div>


            <div v-else-if="step == 2" class="w-full flex flex-col gap-2 justify-center">
                <div class="flex w-full justify-center">
                    <InputConfirmation  
                        @complete="enviarCodigo($event)"
                    />
                </div>

            
                <span class="text-sm text-start flex items-center gap-1">
                    Não recebeu o código? 
                    <div v-if="resendLoading" class="flex items-center gap-1 text-grayScale-500">
                        <Icon nameIcon="ArrowPathIcon" class="w-4 h-4 animate-spin" />
                        <span>Enviando...</span>
                    </div>
                    <span v-else-if="countdown > 0" class="text-grayScale-400">
                        {{ formattedCountdown }}
                    </span>
                    <button v-else @click="reenviarCodigo" class="text-primary underline px-1 hover:text-primary-dark">
                        Reenviar
                    </button>
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
            class="bg-primary hover:opacity-80 duration-200 disabled:bg-grayScale-500 w-full rounded-md h-12 shadow flex justify-center items-center" 
            @click="() => enviarCodigo()"
            :disabled="loading">
                <span v-if="!loading" class="text-primary-light font-semibold">{{stepInfo.textoBotao}}</span>
                <Icon v-else nameIcon="ArrowPathIcon" class="text-white animate-spin"></Icon>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
import type { Campo } from "~/types/formulario";
import BackButton from "@/components/BackButton/index.vue";
import Icon from "@/components/Icon/index.vue"; // Ensure Icon is imported

const router = useRouter();

const step = ref(1)

const code = ref('')

const loading = ref(false)
const resendLoading = ref(false)
const countdown = ref(0)
let timer: NodeJS.Timeout | null = null

const stepperSteps = [
    { label: 'Identificação' },
    { label: 'Informar código' },
    { label: 'Redefinir senha' }
]

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

const toast = useToast();

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

function startCountdown() {
    countdown.value = 60 // 60 seconds
    if (timer) clearInterval(timer)
    timer = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--
        } else {
            if (timer) clearInterval(timer)
        }
    }, 1000)
}

const formattedCountdown = computed(() => {
    const minutes = Math.floor(countdown.value / 60)
    const seconds = countdown.value % 60
    return `${minutes}min ${seconds.toString().padStart(2, '0')}seg`
})

async function enviarCodigo(codigo?: string){
    validarFormulario()

    if (!formValido.value) return

    if(step.value == 1){
        const { data: dataRecovery, error: errorRecovery, execute: executeRecovery, response: responseRecovery } = useApi('post', '/recovery')
        
        loading.value = true
        await executeRecovery({"identifier": form.value.email})
        loading.value = false

        if(!errorRecovery.value && dataRecovery.value) {
            step.value++
            startCountdown()
        }
        else {
            if(responseRecovery.value.status == '404'){                
                toast.error({mensagem: "E-mail não encontrado"} )
            }
        }
        return
    }


    if (step.value == 2){
        const { data: dataCheckCode, loading:loadingCheckCode, error: errorCheckCode, execute: executeCheckCode } = useApi('post', '/chkCode')
        
        code.value = codigo ?? ''
        
        loading.value = true
        await executeCheckCode({code: code.value})
        loading.value = false

        if(dataCheckCode.value && !errorCheckCode.value){
            step.value++
        } else{
            toast.error({mensagem:"Código inválido"})
        }
        return
    }

    if(step.value == 3) confirmarNovaSenha()
}

async function reenviarCodigo() {
    if (countdown.value > 0 || resendLoading.value) return

    const { data: dataRecovery, error: errorRecovery, execute: executeRecovery } = useApi('post', '/recovery')
    
    resendLoading.value = true
    await executeRecovery({"identifier": form.value.email})
    resendLoading.value = false

    if(!errorRecovery.value && dataRecovery.value) {
        toast.success({ mensagem: "Código reenviado com sucesso!" })
        startCountdown()
    } else {
        toast.error({ mensagem: "Erro ao reenviar código." })
    }
}

async function confirmarNovaSenha(){
    if (form.value.password !== form.value.confirmarSenha) {
        erros.value.confirmarSenha = "As senhas não coincidem"
        return
    }

    const { data: dataAuth, loading:loadingAuth, error: errorAuth, execute: executeAuth } = useApi('post', '/auth2r')

    loading.value = true
    await executeAuth({code: code.value, new_password: form.value.password});
    loading.value = false
    
    if(dataAuth.value && !errorAuth.value) {
        toast.success({mensagem: 'Senha alterada com sucesso'})
        router.push('/login')
    } else toast.error({mensagem: 'Ocorreu um erro'})
}

function voltar(){
    if(step.value == 1){
        router.go(-1)
    } 
    else if(step.value == 2){
        step.value--
    }
    else if(step.value == 3){
        step.value = 1
    }
}
</script>

<style scoped>

</style>