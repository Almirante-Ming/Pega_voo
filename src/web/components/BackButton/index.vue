<template>
  <button 
    @click="handleClick" 
    class="flex items-center justify-center p-1 rounded-lg bg-grayScale-100 hover:bg-grayScale-300 text-grayScale-700 transition-colors shadow-sm"
    title="Voltar"
  >
    <Icon nameIcon="ChevronLeftIcon" class="size-5" />
  </button>
</template>

<script setup lang="ts">
import Icon from "../Icon/index.vue";
const router = useRouter();

const props = defineProps<{
  to?: string;
  action?: () => void;
}>();

function handleClick() {
  if (props.action) {
    props.action();
  } else if (props.to) {
    router.push(props.to);
  } else {
    router.go(-1);
  }
}
</script>

<style scoped></style>
