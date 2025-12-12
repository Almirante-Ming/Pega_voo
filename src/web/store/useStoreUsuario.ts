// stores/useStoreDeUsuario.js
import { defineStore } from 'pinia';
import { onMounted } from 'vue';  // Importando onMounted para garantir que o token seja carregado na montagem

export const useStoreDeUsuario = defineStore('usuario', () => {
  // State
  const accessToken = ref();
  const tokenExpirationTime = ref();

  // Função para obter o token
  const getToken = () => accessToken.value;

  // Função para verificar se o token é válido
  const isTokenExpired = () => {
    if (!tokenExpirationTime.value) return true; 
    return Date.now() > tokenExpirationTime.value;
  };

  // Função para definir o token e salvar no localStorage com a expiração
  const setToken = (token) => {
    const expirationTime = Date.now() + 30 * 60 * 1000;
    accessToken.value = token;
    tokenExpirationTime.value = expirationTime;

    // Salvar o token e a hora de expiração no localStorage
    localStorage.setItem('access_token', token);
    localStorage.setItem('token_expiration', expirationTime);
  };

  // Função para carregar o token do localStorage, se válido
  const loadTokenFromStorage = () => {
    const storedToken = localStorage.getItem('access_token');
    const storedExpirationTime = localStorage.getItem('token_expiration');

    if (storedToken && storedExpirationTime) {
      tokenExpirationTime.value = parseInt(storedExpirationTime);
      // Verifica se o token não expirou
      if (Date.now() < tokenExpirationTime.value) {
        accessToken.value = storedToken;
      } else {
        clearToken();
      }
    }
  };

  // Função para limpar o token (no state e localStorage)
  const clearToken = () => {
    accessToken.value = null;
    tokenExpirationTime.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_expiration');
  };

  // Carregar o token quando o store for instanciado
  onMounted(() => {
    loadTokenFromStorage();
  });

  // Retornar todas as funções (getter, setter e funções auxiliares)
  return {
    getToken,
    setToken,
    loadTokenFromStorage,
    clearToken,
    isTokenExpired,
  };
});
