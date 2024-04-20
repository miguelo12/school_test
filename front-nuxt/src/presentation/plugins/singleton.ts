import { Singletons } from '@Domain/inversify.config'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      Singletons: Singletons,
    },
  }
})
