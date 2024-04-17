// import this after install `@mdi/font` package
import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'
import { createVuetify, type ThemeDefinition } from 'vuetify'

const myTheme: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#3f51b5', // your primary color
    secondary: '#b0bec5', // your secondary color
    accent: '#8c9eff', // your accent color
  },
}

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    ssr: false,
    theme: {
      defaultTheme: 'myTheme',
      themes: {
        myTheme,
      },
    },
  })
  app.vueApp.use(vuetify)
})
