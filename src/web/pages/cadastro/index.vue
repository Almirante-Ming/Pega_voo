<template lang="">
  <div>

    <div v-if="step === 1">
      <div class="flex flex-col gap-1.5 mb-4">
        <div class="flex gap-1.5 items-center">
          <BackButton />
          <p class="text-2xl font-semibold">Criar sua conta</p>
        </div>
        <p class="text-grayScale-600">Informe seus dados para prosseguirmos!</p>
      </div>

      
      <Input
        v-for="(campo, index) in formularios"
        :key="index"
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

      <button
        class="bg-primary disabled:bg-grayScale-600 text-white w-full h-12 shadow rounded-md flex justify-center items-center duration-200 hover:opacity-80 mt-8"
        @click="nextStep"
      >
        <span>Prosseguir</span>
      </button>
    </div>

    <div v-if="step === 2" class="space-y-4">
      <div>
        <h2 class="text-xl font-semibold">Definir senha</h2>
        <p class="text-sm text-gray-600">Agora escolha sua senha para completar o cadastro</p>
      </div>

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

      <button
        class="bg-primary disabled:bg-grayScale-600 text-primary-light w-full h-12 shadow rounded-md flex justify-center items-center duration-200 hover:opacity-80"
        @click="cadastrar"
      >
        <span>Cadastrar</span>
      </button>
    </div>
  </div>
</template>


<script setup lang="ts">

import { useForm } from "@/composables/useForm";
import { atualizarFormulario } from "@/functions/atualizarFormulario";
    import { useToast } from "@/composables/useToast";
import BackButton from "@/components/BackButton/index.vue";

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
        propriedade: "full_name",
        tipoDeInput: "nome",
        validacao: "nome",
        obrigatorio: true,
        placeholder: "Seu nome"
    },
    {
        label: "Data de nascimento",
        propriedade: "birth_date",
        validacao: "data",
        tipoDeInput: "data",
        obrigatorio: true,
    },
    {
        label: "Celular",
        propriedade: "phone_number",
        tipoDeInput: "telefone",
        validacao: "telefone",
        obrigatorio: true,
    },
    {
        label: "E-mail",
        propriedade: "email",
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

const { form, erros, formValido, validarCampo, validarFormulario } = useForm(["full_name", "cpf", "birth_date", "phone_number", "email", "gender"], ["senha", "confirmarSenha"]);
const { data, loading, error, execute } = useApi('post', '/register/')
const toast = useToast();

// Cria a função de atualização do formulário usando o helper componentizado
const atualizarForm = atualizarFormulario(form, validarCampo);

const step = ref(1) 

function nextStep() {
    validarFormulario()
    if (!formValido.value) return
    step.value = 2
    console.log(form.value)
    console.log(erros.value)
}

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

const router = useRouter()

async function cadastrar() {
  validarFormulario()
  if (!formValido.value) return

  if (form.value.password !== form.value.confirmarSenha) {
    erros.value.confirmarSenha = "As senhas não coincidem"
    return
  }

  const body = {...form.value}

  delete body.confirmarSenha

  await execute(body)

  if (!error.value && data.value){
    toast.success({mensagem: 'Cadastrado com sucesso!'})
    router.push('/login')
  }else{
    toast.error({mensagem: 'Não foi possivel cadastrar!'})
  }
}

</script>
