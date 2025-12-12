import { ref } from 'vue'

export interface ToastOptions {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
}

export interface ToastTypeOptions {
  mensagem: string
  titulo?: string
  duracao?: number
}

interface ToastItem extends ToastOptions {
  id: number
  visible: boolean
}

const toasts = ref<ToastItem[]>([])
let toastId = 0

export function useToast() {
  function show(options: ToastOptions) {
    clear()
    
    const id = ++toastId
    const toast: ToastItem = {
      id,
      visible: true,
      type: options.type || 'info',
      title: options.title,
      message: options.message,
      duration: options.duration || 5000
    }

    toasts.value.push(toast)

    const duration = toast.duration ?? 5000
    if (duration > 0) {
      setTimeout(() => {
        remove(id)
      }, duration)
    }

    return id
  }


//   Mostra um toast de sucesso
  function success(options: ToastTypeOptions | string) {
    const opts = typeof options === 'string' 
      ? { mensagem: options } 
      : options

    return show({
      type: 'success',
      title: opts.titulo || 'Sucesso!',
      message: opts.mensagem,
      duration: opts.duracao
    })
  }


//   Mostra um toast de erro
  function error(options: ToastTypeOptions | string) {
    const opts = typeof options === 'string' 
      ? { mensagem: options } 
      : options

    return show({
      type: 'error',
      title: opts.titulo || 'Erro!',
      message: opts.mensagem,
      duration: opts.duracao
    })
  }


//   Mostra um toast de atenção
  function warning(options: ToastTypeOptions | string) {
    const opts = typeof options === 'string' 
      ? { mensagem: options } 
      : options

    return show({
      type: 'warning',
      title: opts.titulo || 'Atenção!',
      message: opts.mensagem,
      duration: opts.duracao
    })
  }


//   Mostra um toast de informativo
  function info(options: ToastTypeOptions | string) {
    const opts = typeof options === 'string' 
      ? { mensagem: options } 
      : options

    return show({
      type: 'info',
      title: opts.titulo,
      message: opts.mensagem,
      duration: opts.duracao
    })
  }


//   Mostra um toast específico
  function remove(id: number) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1 && toasts.value[index]) {
      toasts.value[index].visible = false
      setTimeout(() => {
        const currentIndex = toasts.value.findIndex(t => t.id === id)
        if (currentIndex > -1) {
          toasts.value.splice(currentIndex, 1)
        }
      }, 300)
    }
  }


//   Remove qualquer toast
  function clear() {
    toasts.value = []
  }

  return {
    toasts,
    show,
    success,
    error,
    warning,
    info,
    remove,
    clear
  }
}
