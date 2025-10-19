// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  compatibilityDate: "2024-07-15",
  devtools: { enabled: true },
  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],
  css: ["~/assets/css/main.css"],
  imports: {
    dirs: ["store"],
  },
  ssr: false,
  app: {
    head: {
      title: "Pega voo",
      script: [{ defer: true }],
      link: [{ rel: "icon", href: "favicon.ico" }],
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000",
    },
  },
});
