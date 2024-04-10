import { fetchCreateUser, fetchLogIn, fetchLogOut } from "~/services/authService"
import { useStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: useStorage('token', false),
        is_authenticated: useStorage('is_authenticated', false),
        username: useStorage('username', '')
    }),
    actions: {
        async createUser(username: string, password: string) {
            let is_failed = false
            const { _, message } = await fetchCreateUser(username, password).catch(
                (err) => {
                    is_failed = true
                    return err.data
                }
            )
            return { message, is_failed }
        },
        async logIn(username: string, password: string) {
            const { data, message } = await fetchLogIn(username, password).catch(
                (err) => err.data
            )

            if (data && data.token) {
                this.token = data.token
                this.username = username
                this.is_authenticated = true
                navigateTo('/')
            } else {
                this.is_authenticated = false
                this.username = ''
            }

            return message
        },
        async logOut() {
            let token: string | null = localStorage.getItem('token')
            if (!token) return
            await fetchLogOut(token).catch(
                (err) => err.data
            )
            this.is_authenticated = false
            localStorage.clear()
            navigateTo('/login')
        }
    }
})