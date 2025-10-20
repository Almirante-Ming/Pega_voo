<template>
  <div class="bg-background min-h-screen  flex items-center flex-col">
    <Header />
    <div class="px-2.5 mt-2 pb-10 w-full max-w-[1100px]">
      <slot />
    </div>
  </div>
</template>

<script setup>
</script>

<style>
.dp__theme_dark {
  --dp-background-color: var(--input-100);
  --dp-text-color: var(--grayScale-700);
  --dp-border-radius: 8px;
  --dp-border-color-focus: var(--primary);
  --dp-border-color-hover: var(--primary);
  --dp-border-color: var(--input-200);
}

.dp__theme_dark .dp__input {
  padding: 10px 36px;
  font-size: 15px;
}
</style>