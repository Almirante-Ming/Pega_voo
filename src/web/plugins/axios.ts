import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  const axiosInstance = axios.create({
    baseURL: config.public.apiBase,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Interceptor para adicionar token de autenticação (opcional)
  axiosInstance.interceptors.request.use((config) => {
    // const token = useCookie('token').value
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  })

  // Interceptor para tratamento de erros (opcional)
  axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      // Tratamento de erros global
      return Promise.reject(error)
    }
  )

  return {
    provide: {
      axios: axiosInstance
    }
  }
})