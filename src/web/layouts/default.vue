<template>
  <div class="bg-background min-h-screen flex items-center flex-col">
    <Header />
    <div class="px-2.5 md:px-5 pt-3.5 pb-10 w-full min-h-full max-w-[1100px]">
      <slot />
    </div>
    <!-- Toast Container -->
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/Toast/ToastContainer.vue'
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
  padding: 8px 36px;
  font-size: 15px;
}
</style>