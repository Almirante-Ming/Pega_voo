<template>
    <div v-if="visivel" class="mb-5">
        <label
			v-if="props.label"
			for="default-input"
			class="mb-1 block font-medium text-grayScale-800"
			>{{ props.label }}
		</label>
        <VueDatePicker v-model="inputDateRange" class="dp__theme_dark" :dark="true" :format="formatacaoData" :enableTime="true" :time24hr="true" />
		<span v-if="errorMessage" class="text-[#ff3b3b] text-sm">{{ errorMessage }}</span>
    </div>
</template>

<script setup lang="ts">
    import VueDatePicker from '@vuepic/vue-datepicker';
    import '@vuepic/vue-datepicker/dist/main.css'
    
    interface Props {
        label?: string;
        tipoDeDado?: string; //input, select
        valorPadrao?: any;
        placeholder?: string;
        obrigatorio?: boolean;
        visivel?: boolean;
        habilitado?: boolean;
        propriedade?: string;
        valor?:any
        hasError:boolean;
        errorMessage:string;
    }
    const props = withDefaults(defineProps<Props>(), {
        tipoDeDado: "string", //string, number, boolean
        habilitado: true,
        visivel: true,
        obrigatorio: false
    });

    const emits = defineEmits(["inputEmitValue"]);

    const inputDateRange = ref()
    watch(() => inputDateRange.value, (value: any) => {        
        handleInput(value)
    });

    const formatacaoData = (date: any) => {
        const formatDateWithTime = (d: Date) => {
            const day = d.getDate();
            const month = d.getMonth() + 1;
            const year = d.getFullYear();
            const hours = d.getHours();
            const minutes = d.getMinutes();
            return `${day < 10 ? '0' + day : day}/${month < 10 ? '0' + month : month}/${year} ${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes}`;
        };

        if (Array.isArray(date)) {
            const formattedDates = date.map(d => (d ? formatDateWithTime(d) : ''));
            return formattedDates.filter(Boolean).join(' - ');
        } else if (date) {
            return formatDateWithTime(date);
        } else {
            return '';
        }
    };

    const handleInput = (event: any) => {    
        if (event) { 
            const date = new Date(event);

            const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;

            emits("inputEmitValue", formattedDate);
        }
    };

    onMounted(() => {
        if (props.valorPadrao) {
            inputDateRange.value = props.valorPadrao;
        }

        if (props.valor) {
            const parsedDate = parseDateString(props.valor);
            if (parsedDate) {
                inputDateRange.value = parsedDate;
            }
        }
    });

    // Função para converter "DD/MM/YYYY - HH:mm" para um objeto Date
    const parseDateString = (dateString: string) => {
        const [datePart, timePart] = dateString.split(" - ");
        const [day, month, year] = datePart.split("/").map(Number);
        const [hours, minutes] = timePart.split(":").map(Number);

        // Verifica se todos os valores são válidos antes de criar o Date
        if (!isNaN(day) && !isNaN(month) && !isNaN(year) && !isNaN(hours) && !isNaN(minutes)) {
            return new Date(year, month - 1, day, hours, minutes);
        }
        return null; // Retorna null se a data não puder ser convertida
    };

</script>

<style scoped>

</style>