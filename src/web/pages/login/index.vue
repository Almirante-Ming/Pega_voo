<template>
    <div class="h-[85dvh] w-full flex flex-col items-center justify-center px-4 text-grayScale-800">
        <div class="w-full flex flex-col items-center gap-1.5">
           <p class="text-2xl font-semibold">Malas Prontas?</p>
           <p class="text-lg">Faça login para continuar</p>
        </div>

        <div class="w-full flex flex-col gap-1 mt-6">
            <Input
                :tipoDeComponente="email.tipoDeInput"
                :tipoDeInput="email.tipoDeInput" 
                :validacao="email.validacao" 
                :obrigatorio="email.obrigatorio"
                :label="email.label"
                :propriedade="email.propriedade" 
                :hasError="Boolean(errors[email.propriedade])"
                :errorMessage="errors[email.propriedade]"
                @emite-valor="atualizarFormulario(email.propriedade, $event, email.validacao)"
            />
            <Input
                :tipoDeComponente="senhaVisivel ? 'string' : 'senha'"
                :tipoDeInput="senhaVisivel ? 'string' : 'senha'" 
                :obrigatorio="senha.obrigatorio"
                :label="senha.label"
                :propriedade="senha.propriedade" 
                :hasError="Boolean(errors[senha.propriedade])"
                :errorMessage="errors[senha.propriedade]"
                :icone="senhaVisivel ? 'EyeIcon' : 'EyeSlashIcon'"
                :placeholder="senha.placeholder"
                :marginBottom="false"
                @emitClick="senhaVisivel = !senhaVisivel"
                @emiteValor="atualizarFormulario(senha.propriedade, $event, '')"
            />
            <div class="w-full flex justify-end">
                <button @click="router.push('/recuperarSenha')" class="text-sm text-end underline text-grayScale-600 duration-150 hover:text-primary-light">Esqueci minha senha</button>
            </div>
        </div>

        <div class="w-full flex flex-col gap-2 mt-6">
            <button @click="login" :disabled="loading" class="bg-primary disabled:bg-grayScale-600 text-white w-full h-12 shadow rounded-md flex justify-center items-center duration-200 hover:bg-primary-light">
                <span v-if="!loading" class="font-semibold tracking-wide">Entrar</span>
                <Icon v-else name-icon="ArrowPathIcon" class="animate-spin text-grayScale-100"></Icon>
            </button>

            <button class="bg-gray-100 w-full h-12 flex justify-center items-center gap-3 shadow-md rounded-md hover:bg-white text-gray-700">
                <img src="@/assets/images/google-icon.webp" class="w-5 h-5"></img>
                <span class="font-semibold">Entre com o Google</span>
            </button>

            <button @click="router.push('/cadastro')" class="text-center text-lg mt-2 duration-150 hover:text-primary-light">
                ou <span class="underline font-semibold">Cadastre-se</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useForm } from "@/composables/useForm";

    const router = useRouter();

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
    
    const senhaVisivel = ref(false)
    
    const { data, loading, error, execute } = useApi('post', '/login', { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })

    const { form, errors, formIsValid, handleValidateField, handleValidateFields } = useForm(['username', 'password'], []);

    async function login(){
        const params = new URLSearchParams();
        params.append('username', form.value.username);
        params.append('password', form.value.password);

        await execute(params.toString());
    }

    function atualizarFormulario(field: string, value: any, validar?:string){
        form.value[field] = value?.target?.value
            ? value.target.value
            : typeof value === "boolean"
            ? value
            : typeof value === "string" || typeof value === "number"
            ? value
            : value?.chave ?? ""
        
        
        if(validar){        
            handleValidateField(field, validar);
        } else{
            handleValidateField(field);
        }
    }

</script>