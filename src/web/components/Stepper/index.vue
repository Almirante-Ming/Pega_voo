<template>
    <div class="w-full">
        <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-grayScale-600">Etapa {{ currentStep }}/{{ steps.length }}</span>
        </div>
        
        <div class="flex items-center gap-2">
            <div 
                v-for="(step, index) in steps" 
                :key="index"
                class="flex-1 flex flex-col gap-2"
            >
                <div class="flex items-center gap-2">
                    <div 
                        class="h-1 w-full rounded-full transition-colors duration-300"
                        :class="index + 1 <= currentStep ? 'bg-success' : 'bg-grayScale-300'"
                    ></div>
                </div>
                
                <span 
                    class="text-xs transition-colors duration-300"
                    :class="index + 1 <= currentStep ? 'text-primary font-medium' : 'text-grayScale-500'"
                >
                    {{ step.label }}
                </span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
interface Step {
    label: string;
}

interface Props {
    steps: Step[];
    currentStep: number;
}

defineProps<Props>();
</script>

<style scoped>
</style>