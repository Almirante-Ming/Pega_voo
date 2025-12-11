<template>
  <div class="flex gap-3 w-full max-w-[500px]">
      <input
        v-for="(digit, index) in digits"
        :key="index"
        :ref="(el) => setInputRef(el, index)"
        v-model="digits[index]"
        type="text"
        inputmode="numeric"
        maxlength="1"
        class=" h-14 md:h-20 min-w-0 flex-1 text-center text-xl font-semibold border border-grayScale-400 rounded-lg bg-grayScale-50 text-grayScale-900 transition-all outline-none focus:border-primary focus:drop-shadow disabled:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-60"
        :class="{ 'border-blue-500 bg-blue-50': digits[index] }"
        @input="handleInput(index, $event)"
        @keydown="handleKeyDown(index, $event)"
        @paste="handlePaste"
        @focus="handleFocus(index)"
      />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

interface Props {
  length?: number
  autoFocus?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  length: 6,
  autoFocus: true
})

const emit = defineEmits<{
  complete: [code: string]
  change: [code: string]
}>()

const digits = ref<string[]>(Array(props.length).fill(''))
const inputRefs = ref<(HTMLInputElement | null)[]>([])

const setInputRef = (el: any, index: number) => {
  if (el) {
    inputRefs.value[index] = el as HTMLInputElement
  }
}

const handleInput = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const value = target.value

  // Aceita apenas números
  if (value && !/^\d$/.test(value)) {
    digits.value[index] = ''
    return
  }

  digits.value[index] = value

  // Move para o próximo campo se preencheu
  if (value && index < props.length - 1) {
    inputRefs.value[index + 1]?.focus()
  }

  // Verifica se todos os campos estão preenchidos
  checkComplete()
  
  // Emite evento de mudança
  emitChange()
}

const handleKeyDown = (index: number, event: KeyboardEvent) => {
  // Backspace: volta para o campo anterior se o atual está vazio
  if (event.key === 'Backspace' && !digits.value[index] && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
  
  // Seta esquerda: volta para o campo anterior
  if (event.key === 'ArrowLeft' && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
  
  // Seta direita: avança para o próximo campo
  if (event.key === 'ArrowRight' && index < props.length - 1) {
    inputRefs.value[index + 1]?.focus()
  }
}

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text') || ''
  const numbers = pastedData.replace(/\D/g, '').slice(0, props.length)
  
  numbers.split('').forEach((num, index) => {
    if (index < props.length) {
      digits.value[index] = num
    }
  })
  
  // Foca no próximo campo vazio ou no último
  const nextEmptyIndex = digits.value.findIndex(d => !d)
  const focusIndex = nextEmptyIndex !== -1 ? nextEmptyIndex : props.length - 1
  inputRefs.value[focusIndex]?.focus()
  
  checkComplete()
  emitChange()
}

const handleFocus = (index: number) => {
  // Seleciona o conteúdo ao focar
  inputRefs.value[index]?.select()
}

const checkComplete = () => {
  const isComplete = digits.value.every(d => d !== '')
  if (isComplete) {
    const code = digits.value.join('')
    emit('complete', code)
  }
}

const emitChange = () => {
  const code = digits.value.join('')
  emit('change', code)
}

const clear = () => {
  digits.value = Array(props.length).fill('')
  inputRefs.value[0]?.focus()
}

const focus = () => {
  const firstEmptyIndex = digits.value.findIndex(d => !d)
  const focusIndex = firstEmptyIndex !== -1 ? firstEmptyIndex : 0
  inputRefs.value[focusIndex]?.focus()
}

// Expõe métodos para o componente pai
defineExpose({
  clear,
  focus
})

onMounted(() => {
  if (props.autoFocus) {
    inputRefs.value[0]?.focus()
  }
})
</script>