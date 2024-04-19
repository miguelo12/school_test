// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  ssr: false,
  srcDir: 'src/presentation/',
  devtools: { enabled: true },
  plugins: [],
  runtimeConfig: {
    public: {
      apiBaseUrl: 'http://localhost:5000',
    },
  },
  imports: {
    dirs: [
    ],
  },
  build: {
    transpile: ['vuetify'],
  },
  modules: [
    '@vueuse/nuxt',
    '@pinia/nuxt',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error porque quizas no exista
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    '@nuxt/eslint',
  ],
  pinia: {
    storesDirs: ['./src/domain/stores/**'],
  },
  nitro: {
    esbuild: {
      options: {
        tsconfigRaw: {
          compilerOptions: {
            experimentalDecorators: true,
          },
        },
      },
    },
  },
  vite: {
    esbuild: {
      tsconfigRaw: {
        compilerOptions: {
          experimentalDecorators: true,
        },
      },
    },
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  eslint: {
  },
  app: {
    head: {
      viewport: 'width=device-width,initial-scale=1',
      link: [
        { rel: 'icon', href: '/favicon.ico', sizes: 'any' },
        // { rel: 'icon', type: 'image/svg+xml', href: '/nuxt.svg' },
        // { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
      ],
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '' },
      ],
    },
  },
  typescript: {
    typeCheck: false,
  },
})
