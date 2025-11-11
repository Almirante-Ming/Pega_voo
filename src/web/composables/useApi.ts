import type { AxiosRequestConfig } from "axios";

type Method = "get" | "post" | "put" | "delete";

export function useApi(
  method: Method,
  route: string,
  options?: AxiosRequestConfig
) {
  const { $axios } = useNuxtApp();
  const data = ref<any>(null);
  const error = ref<any>(null);
  const loading = ref(false);
  const response = ref<any>(null)
  
  async function execute(body?: object) {
    try {
      loading.value = true;
      /* Quando vier body, é algum método diferente do get. Do contrário, é get. */
      if (body) response.value = await $axios[method](route, body, options);
      else response.value = await $axios[method](route, options);

      data.value = response.value.data;
    } catch (e: any) {
      // useSentry(e)
      // const sentry = useSentry();

      const err = new Error();
      if (e?.response?.data?.errors?.[0].message) err.name = `Status ${e?.response?.status} - ${e?.response?.data?.errors[0].message}`;
      else err.name = `Status ${e?.response?.status}`;
      err.message = JSON.stringify(e?.response?.data?.errors);

      //@ts-ignore
      // sentry.captureException(err);
      error.value = e.response.data;
    } finally {
      loading.value = false;
    }
  }

  return {
    data: computed(() => data.value),
    error,
    loading: computed(() => loading.value),
    execute,
    response: computed(() => response.value)
  };
}
