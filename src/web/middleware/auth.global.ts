
import { useStoreDeUsuario } from "~/store/useStoreUsuario";

export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) {
        const store = useStoreDeUsuario();

        store.loadTokenFromStorage();

        const publicRoutes = ['/login', '/cadastro', '/recuperarSenha'];
        const isPublic = publicRoutes.includes(to.path);
        const hasToken = !!store.getToken() && !store.isTokenExpired();

        if (!hasToken && !isPublic) {
            return navigateTo('/login');
        }
        if (hasToken && isPublic) {
            return navigateTo('/');
        }
    }
});
