import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import axios from 'axios'
import { computed, ref } from 'vue'

type Method = 'get' | 'post' | 'put' | 'delete'

interface UseApiOptions extends AxiosRequestConfig {
  baseURL?: string
}

export default function useApi(
  method: Method,
  route: string,
  options?: UseApiOptions,
  body?: object
) {
  const data = ref<any>(null)
  const error = ref<any>(null)
  const loading = ref(false)
  const response = ref<any>(null)

  if (!options?.baseURL) {
    console.log('Nenhuma baseURL fornecida, playComponents')
    console.error('Nenhuma baseURL fornecida, playComponents')
    error.value = 'Nenhuma baseURL fornecida'

    return {
      data: computed(() => data.value),
      error,
      loading: computed(() => loading.value),
      execute: async () => {
        console.error('Não é possível executar requisição sem baseURL')
      },
      response: computed(() => response.value)
    }
  }

  const axiosInstance: AxiosInstance = axios.create({
    baseURL: options.baseURL,
    timeout: 300000,
    headers: {
      'Content-Type': 'application/json'
    },
    ...options
  })

  axiosInstance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('authToken')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  axiosInstance.interceptors.response.use(
    (response) => {
      return response
    },
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('authToken')
      }
      return Promise.reject(error)
    }
  )

  async function execute() {
    try {
      loading.value = true
      error.value = null

      /* Quando vier body, é algum método diferente do get. Do contrário, é get. */
      if (body) {
        response.value = await axiosInstance[method](route, body, options)
      } else {
        response.value = await axiosInstance[method](route, options)
      }

      data.value = response.value.data
    } catch (e: any) {
      const err = new Error()
      if (e?.response?.data?.errors?.[0]?.message) {
        err.name = `Status ${e?.response?.status} - ${e?.response?.data?.errors[0].message}`
      } else {
        err.name = `Status ${e?.response?.status}`
      }
      err.message = JSON.stringify(e?.response?.data?.errors)

      error.value = e
    } finally {
      loading.value = false
    }
  }

  return {
    data: computed(() => data.value),
    error,
    loading: computed(() => loading.value),
    execute,
    response: computed(() => response.value)
  }
}
