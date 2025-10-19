<template>
  <component :is="iconComponent" :class="clsx('size-6 text-primary', props.class)" />
</template>

<script setup lang="ts">
import * as HeroIcons from "@heroicons/vue/20/solid";
import clsx from "clsx";

interface Props {
  nameIcon: keyof typeof HeroIcons;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  nameIcon: "HomeIcon",
  class: "",
});

const iconComponent = computed(() => {
  return HeroIcons[props.nameIcon] || HeroIcons.CommandLineIcon;
});
</script>

<style scoped></style>