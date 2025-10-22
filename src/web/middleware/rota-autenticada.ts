import { useStoreDeUsuario } from "~/store/useStoreUsuario";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const storeDeUsuario = useStoreDeUsuario();  

  storeDeUsuario.loadTokenFromStorage();

  if (!storeDeUsuario.getToken() || storeDeUsuario.isTokenExpired()) {
    return navigateTo('/login');
  }
});
