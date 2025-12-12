<template>
  <div class="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex justify-center items-center flex-col gap-3 pointer-events-none">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="pointer-events-auto"
    >
      <Toast
        :type="toast.type"
        :title="toast.title"
        :message="toast.message"
        :duration="toast.duration"
        :visible="toast.visible"
        @close="remove(toast.id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/useToast'
import Toast from '@/components/Toast/index.vue'

const { toasts, remove } = useToast()
</script>
