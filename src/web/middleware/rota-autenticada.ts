import { useStoreDeUsuario } from "~/store/useStoreUsuario"; // Corrija o caminho para ~/stores

export default defineNuxtRouteMiddleware(async (to, from) => {
  const storeDeUsuario = useStoreDeUsuario();  

  // Carregar o token do localStorage antes de qualquer verificação
  storeDeUsuario.loadTokenFromStorage();

  // Log para verificar se o token foi carregado corretamente
  console.log("Token carregado:", storeDeUsuario.getToken());  

  // Verificar se o token não existe ou se está expirado
  if (!storeDeUsuario.getToken() || storeDeUsuario.isTokenExpired()) {
    return navigateTo('/login'); // Redirecionar para o login se o token for inválido ou expirado
  }
});
