import 'reflect-metadata'
import { useStorage } from '@vueuse/core'
import type { Singletons } from '@Domain/inversify.config'
import AuthUseCase from '@Domain/useCases/authUseCase'

const singletons = useNuxtApp().$Singletons as typeof Singletons

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: useStorage('token', ''),
    is_authenticated: useStorage('is_authenticated', false),
    username: useStorage('username', ''),
  }),
  actions: {
    async createUser(username: string, password: string) {
      const authUseCase = singletons.resolve(AuthUseCase)
      return await authUseCase.createUser(username, password)
    },
    async logIn(username: string, password: string) {
      const authUseCase = singletons.resolve(AuthUseCase)
      const { data, message } = await authUseCase.logIn(username, password)

      if (data && data.token) {
        this.token = data.token
        this.username = username
        this.is_authenticated = true
        navigateTo('/')
      }
      else {
        this.is_authenticated = false
        this.username = ''
      }

      return message
    },
    async logOut() {
      const authUseCase = singletons.resolve(AuthUseCase)
      if (this.token) {
        await authUseCase.logOut(this.token)
      }
      this.is_authenticated = false
      localStorage.clear()
      navigateTo('/login')
    },
  },
})
