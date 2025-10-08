export default defineNuxtPlugin(() => {
  const { initTheme } = useTheme();

  if (import.meta.client) {
    initTheme();
  }
});
