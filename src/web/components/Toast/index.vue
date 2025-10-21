<template>
  <Transition name="toast">
    <div
      v-if="visible"
      :class="[
        'flex items-start gap-3 p-4 rounded-lg shadow-lg max-w-md min-w-[320px]',
        'animate-slide-in',
        toastClasses
      ]"
      role="alert"
    >
      <!-- Ícone -->
      <div class="flex-shrink-0">
        <Icon
          :name-icon="iconName"
          :class="`w-6 h-6 ${iconClasses}`"
        />
      </div>

      <!-- Conteúdo -->
      <div class="flex-1">
        <h3 v-if="title" :class="['font-semibold text-sm mb-1', textClasses]">
          {{ title }}
        </h3>
        <p :class="['text-sm', textClasses]">
          {{ message }}
        </p>
      </div>

      <!-- Botão fechar -->
      <button
        @click="close"
        :class="['flex-shrink-0 hover:opacity-70 transition-opacity', textClasses]"
        aria-label="Fechar"
      >
        <Icon name-icon="XMarkIcon" class="w-5 h-5" />
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
interface Props {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
  visible?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 5000,
  visible: false
})

const emit = defineEmits<{
  close: []
}>()

const visible = ref(props.visible)
let timeoutId: ReturnType<typeof setTimeout> | null = null

// Computed properties para classes baseadas no tipo
const toastClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-600 border border-green-600'
    case 'error':
      return 'bg-red-500 border border-red-600'
    case 'warning':
      return 'bg-yellow-300 border border-yellow-400'
    case 'info':
    default:
      return 'bg-blue-500 border border-blue-600'
  }
})

const textClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-50'
    case 'error':
      return 'text-red-50'
    case 'warning':
      return 'text-yellow-950'
    case 'info':
    default:
      return 'text-blue-50'
  }
})

const iconClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-200'
    case 'error':
      return 'text-red-200'
    case 'warning':
      return 'text-yellow-700'
    case 'info':
    default:
      return 'text-blue-100'
  }
})

const iconName = computed(() => {
  switch (props.type) {
    case 'success':
      return 'CheckCircleIcon'
    case 'error':
      return 'XCircleIcon'
    case 'warning':
      return 'ExclamationTriangleIcon'
    case 'info':
    default:
      return 'InformationCircleIcon'
  }
})

// Funções
function close() {
  visible.value = false
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
  emit('close')
}

function show() {
  visible.value = true
  
  if (props.duration > 0) {
    timeoutId = setTimeout(() => {
      close()
    }, props.duration)
  }
}

// Watch para mudanças na prop visible
watch(() => props.visible, (newValue) => {
  if (newValue) {
    show()
  } else {
    close()
  }
}, { immediate: true })

// Expor funções para uso com ref
defineExpose({
  show,
  close
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}
</style>
