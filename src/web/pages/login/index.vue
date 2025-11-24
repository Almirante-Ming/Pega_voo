<template>
    <div class="h-[85dvh] w-full flex flex-col items-center justify-center text-grayScale-800">
        <div class="w-full flex flex-col items-center gap-1.5">
           <p class="text-2xl font-semibold">Malas Prontas?</p>
           <p class="text-lg">Faça login para continuar</p>
        </div>


        <form class="w-full flex flex-col gap-1 mt-6">
            <Input
                :tipoDeComponente="email.tipoDeInput"
                :tipoDeInput="email.tipoDeInput" 
                :validacao="email.validacao" 
                :obrigatorio="email.obrigatorio"
                :label="email.label"
                :propriedade="email.propriedade" 
                :hasError="Boolean(erros[email.propriedade])"
                :errorMessage="erros[email.propriedade]"
                @emite-valor="atualizarForm(email.propriedade, $event, email.validacao)"
            />
            <Input
                :tipoDeComponente="senhaVisivel ? 'string' : 'senha'"
                :tipoDeInput="senhaVisivel ? 'string' : 'senha'" 
                :obrigatorio="senha.obrigatorio"
                :label="senha.label"
                :propriedade="senha.propriedade" 
                :hasError="Boolean(erros[senha.propriedade])"
                :errorMessage="erros[senha.propriedade]"
                :icone="senhaVisivel ? 'EyeIcon' : 'EyeSlashIcon'"
                :placeholder="senha.placeholder"
                :marginBottom="false"
                @emitClick="senhaVisivel = !senhaVisivel"
                @emiteValor="atualizarForm(senha.propriedade, $event, '')"
            />
            <div class="w-full flex justify-end">
                <button type="button" @click="router.push('/recuperarSenha')" class="text-sm text-end underline text-grayScale-600 duration-150 hover:text-grayScale-900">Esqueci minha senha</button>
            </div>
        </form>


        <div class="w-full flex flex-col gap-2 mt-6">
            <button @click="login" :disabled="loading" class="bg-primary disabled:bg-grayScale-600 text-white w-full h-12 shadow rounded-md flex justify-center items-center duration-200 hover:opacity-80">
                <span v-if="!loading" class="font-semibold text-primary-light tracking-wide">Entrar</span>
                <Icon v-else name-icon="ArrowPathIcon" class="animate-spin text-grayScale-100"></Icon>
            </button>

            <button class="bg-gray-100 w-full h-12 flex justify-center items-center gap-3 shadow-md rounded-md hover:bg-white text-gray-700">
                <img src="@/assets/images/google-icon.webp" class="w-5 h-5"></img>
                <span class="font-semibold">Entre com o Google</span>
            </button>

            <button @click="router.push('/cadastro')" class="text-center text-lg mt-2 text-grayScale-700 duration-150 hover:text-grayScale-900">
                ou <span class="underline font-semibold">Cadastre-se</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useForm } from "@/composables/useForm";
    import { atualizarFormulario } from "@/functions/atualizarFormulario";
    import { useToast } from "@/composables/useToast";
    import { useStoreDeUsuario } from "~/store/useStoreUsuario";

    const router = useRouter();
    const toast = useToast();
    const senhaVisivel = ref(false)

    const email =  {
        label: "E-mail",
        propriedade: "username",
        validacao: "email",
        tipoDeInput: "email",
        obrigatorio: true
    }
    const senha = {
        label: "Senha",
        propriedade: "password",
        obrigatorio: true,
        placeholder: "********"
    }
    
    const { data, loading, error, execute } = useApi('post', '/login', { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })

    const { form, erros, formValido, validarCampo, validarFormulario } = useForm(['username', 'password'], []);

    const atualizarForm = atualizarFormulario(form, validarCampo);

    const storeDeUsuario = useStoreDeUsuario();

    async function login(){
        validarFormulario({ username: 'email' })

        if(!formValido.value) {
            toast.warning({ mensagem: 'Preencha todos os campos corretamente' })
            return 
        }

        const params = new URLSearchParams();
        params.append('username', form.value.username);
        params.append('password', form.value.password);

        try {
            await execute(params.toString());
            
            if (error.value) {
                toast.error({ mensagem: 'Usuário ou senha incorretos', titulo: 'Erro no login' })
                return
            }

            storeDeUsuario.setToken(data.value.access_token)
            
            toast.success({ mensagem: 'Login realizado com sucesso!' })
            router.push('/')
        } catch (err) {
            toast.error({ mensagem: 'Erro ao tentar fazer login. Tente novamente.' })
        }
    }

</script>