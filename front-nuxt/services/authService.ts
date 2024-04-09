interface LogInAPI {
    token: string
}

export async function fetchCreateUser(username: string, password: string) {
    const apiBase = useRuntimeConfig().public.apiBaseUrl
    return await $fetch<BaseAPI<LogInAPI>>(`${apiBase}/user`, {
        method: 'POST',
        body: { username, password },
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export async function fetchLogIn(username: string, password: string) {
    const apiBase = useRuntimeConfig().public.apiBaseUrl
    return await $fetch<BaseAPI<LogInAPI>>(`${apiBase}/auth`, {
        method: 'POST',
        body: { username, password },
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export async function fetchLogOut(jwt: string) {
    const apiBase = useRuntimeConfig().public.apiBaseUrl
    return await $fetch(`${apiBase}/auth`, {
        method: 'delete',
        headers: {
            'Authorization': jwt
        }
    })
}