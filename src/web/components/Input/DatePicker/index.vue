<template>
    <div v-if="visivel" class="mb-5">
        <label
			v-if="props.label"
			for="default-input"
			class="mb-1 block font-medium text-grayScale-800"
			>{{ props.label }}
		</label>
        <VueDatePicker 
            v-model="inputDateRange" 
            :enable-time-picker="mostrarHora" 
            :format="formatacaoData" 
            :time24hr="mostrarHora" 
            :dark="isDark"
            auto-apply
        />
		<span v-if="errorMessage" class="text-[#ff3b3b] text-sm">{{ errorMessage }}</span>
    </div>
</template>

<script setup lang="ts">
    import { useTheme } from '@/composables/useTheme';
    import VueDatePicker from '@vuepic/vue-datepicker';
    import '@vuepic/vue-datepicker/dist/main.css'

    const { isDark } = useTheme();
    
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
        mostrarHora: boolean
    }
    const props = withDefaults(defineProps<Props>(), {
        tipoDeDado: "string",
        habilitado: true,
        visivel: true,
        obrigatorio: false,
        mostrarHora: true
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
            
            if (props.mostrarHora) {
                const hours = d.getHours();
                const minutes = d.getMinutes();
                return `${day < 10 ? '0' + day : day}/${month < 10 ? '0' + month : month}/${year} ${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes}`;
            } else {
                return `${day < 10 ? '0' + day : day}/${month < 10 ? '0' + month : month}/${year}`;
            }
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

            if (props.mostrarHora) {
                const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
                emits("inputEmitValue", formattedDate);
            } else {
                const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
                emits("inputEmitValue", formattedDate);
            }
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

    const parseDateString = (dateString: string) => {
        if (dateString.includes(" - ")) {
            const parts = dateString.split(" - ");
            const datePart = parts[0];
            const timePart = parts[1];
            
            if (datePart && timePart) {
                const [day, month, year] = datePart.split("/").map(Number);
                const [hours, minutes] = timePart.split(":").map(Number);

                if (day && month && year && !isNaN(day) && !isNaN(month) && !isNaN(year) && 
                    hours !== undefined && minutes !== undefined && !isNaN(hours) && !isNaN(minutes)) {
                    return new Date(year, month - 1, day, hours, minutes);
                }
            }
        } else {
            const [day, month, year] = dateString.split("/").map(Number);

            if (day && month && year && !isNaN(day) && !isNaN(month) && !isNaN(year)) {
                return new Date(year, month - 1, day);
            }
        }
        return null;
    };

</script>

<style>
/* Override VueDatePicker variables to match app theme */
.dp__theme_light,
.dp__theme_dark {
   --dp-background-color: var(--input-100);
   --dp-text-color: var(--grayScale-800);
   --dp-hover-color: var(--grayScale-200);
   --dp-hover-text-color: var(--grayScale-900);
   --dp-hover-icon-color: var(--grayScale-900);
   --dp-primary-color: var(--primary);
   --dp-primary-text-color: #ffffff;
   --dp-secondary-color: var(--grayScale-400);
   --dp-border-color: var(--input-200);
   --dp-menu-border-color: var(--input-200);
   --dp-border-color-hover: var(--primary);
   --dp-disabled-color: var(--grayScale-200);
   --dp-scroll-bar-background: var(--grayScale-100);
   --dp-scroll-bar-color: var(--grayScale-400);
   --dp-success-color: var(--success);
   --dp-success-color-disabled: var(--grayScale-400);
   --dp-icon-color: var(--grayScale-400);
   --dp-danger-color: var(--error);
   --dp-highlight-color: var(--primary-light);
   
   /* Sizing */
   --dp-border-radius: 0.5rem; /* rounded-lg */
   --dp-cell-border-radius: 4px;
   --dp-font-family: inherit;
   --dp-font-size: 0.875rem; /* text-sm */
   --dp-preview-font-size: 0.8rem;
   --dp-time-font-size: 0.8rem;
   
   /* Spacing */
   --dp-button-height: 35px;
   --dp-month-year-row-height: 35px;
   --dp-month-year-row-button-size: 35px;
   --dp-button-icon-height: 20px;
   --dp-cell-size: 35px;
   --dp-cell-padding: 5px;
   --dp-common-padding: 10px;
   --dp-input-icon-padding: 35px;
   --dp-input-padding: 10px; 
   --dp-menu-min-width: 260px;
   --dp-action-buttons-padding: 2px 5px;
   --dp-row-margin:  5px 0;
   --dp-calendar-header-cell-padding:  0.5rem;
   --dp-two-calendars-spacing:  10px;
   --dp-overlay-col-padding:  3px;
   --dp-time-inc-dec-button-size:  32px;
   --dp-menu-padding: 6px 8px;
}

/* Specific overrides for input element to match BaseInput exactly */
.dp__input {
    min-height: 42px; /* Matches standard input height */
    background-color: var(--input-100);
    border-color: var(--input-200);
    color: var(--grayScale-800);
}

.dp__input:hover {
    border-color: var(--grayScale-400);
}

.dp__input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 0.06rem var(--primary); /* match ring-primary */
}
</style>