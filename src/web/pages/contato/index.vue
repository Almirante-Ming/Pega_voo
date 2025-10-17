<template>
    <div>
        <Input 
            tipoDeComponente="select"
            tipoDeInput="select"
            :label="selectNamoro.label"
            :model="selectNamoro.model"
            :modelType="selectNamoro.modelType"
            :propriedade="selectNamoro.propriedade"
            @emiteValor="handleChangeForm(selectNamoro.propriedade, $event)"
        />
    </div>
</template>

<script setup lang="ts">
const { form, errors, formIsValid, handleValidateField, handleValidateFields } = useForm(['nome'], ['nomeSocial']);

const selectNamoro = {
    label: "Namora comigo?",
    propriedade: "namora_comigo",
    tipoDeComponente: "select",
    tipoDeInput: "select",
    modelType: "static",
    model: [
        { chave: "sim", descricao: "Sim" },
        { chave: "nao", descricao: "Não" },
        { chave: "talvez", descricao: "Talvez" }
    ]
};

function handleChangeForm(field: string, value: any){
    form.value[field] = value?.target?.value
        ? value.target.value
        : typeof value === "boolean"
        ? value
        : typeof value === "string" || typeof value === "number"
        ? value
        : value?.chave ?? ""
    
    handleValidateField(field);
}

onMounted(()=>{
    // if (dados de edicao) {
    //     const formEdicao = dados de edicao;
    //     const formTransformado = Object.fromEntries(
    //         Object.entries(formEdicao)
    //             .filter(([key, value]) => camposObrigatorios.value.includes(key) || camposOpcionais.value.includes(key))
    //     );

    //     form.value = { ...formTransformado };
    // }
})
</script>

<style scoped>

</style>