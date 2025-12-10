
<template>
  <li>
    <NuxtLink
      :to="to"
      class="flex items-center gap-4 px-4 py-3.5 text-grayScale-700 rounded-xl hover:bg-primary-50 hover:text-primary transition-all duration-200 group"
      active-class="bg-primary-50 text-primary font-semibold"
      @click="$emit('onClick')"
    >
      <Icon 
        :name-icon="iconName as any" 
        class="size-6 text-grayScale-500 group-hover:text-primary transition-colors" 
      />
      <span class="font-medium">{{ label }}</span>
      <Icon 
        name-icon="ChevronRightIcon" 
        class="size-4 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" 
      />
    </NuxtLink>
  </li>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";

defineProps<{
  to: string;
  iconName: string;
  label: string;
}>();

defineEmits<{
  (e: "onClick"): void;
}>();
</script>
