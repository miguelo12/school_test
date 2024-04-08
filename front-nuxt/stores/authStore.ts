import { fetchLogIn, fetchLogOut } from "~/services/authService"

export const useAuthStore = defineStore('auth', {
    state: () => ({
        message: '',
        is_authenticated: false,
        username: ''
    }),
    actions: {
        async logIn(username: string, password: string) {
            const { data, message } = await fetchLogIn(username, password).catch(
                (err) => err.data
            )

            if (data && data.token) {
                localStorage.setItem('token', data.token)
                this.username = username
                this.is_authenticated = true
            } else {
                this.is_authenticated = false
                this.username = ''
            }
            this.message = message
        },
        async logOut() {
            let token: string | null = localStorage.getItem('token')
            if (!token) return
            const { data } = await fetchLogOut(token)
            this.is_authenticated = false
            localStorage.clear()
        }
    }
})