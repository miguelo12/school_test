import type { authLoginModel } from '../model/authModel'
import type { BaseModel } from '../model/baseModel'
import BaseAPI from './baseApi'

class AuthApi extends BaseAPI {
  async CreateUser(username: string, password: string) {
    return await $fetch<BaseModel<object>>(`${this.apiBase}/user`, {
      method: 'POST',
      body: { username, password },
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  async logIn(username: string, password: string) {
    return await $fetch<BaseModel<authLoginModel>>(`${this.apiBase}/auth`, {
      method: 'POST',
      body: { username, password },
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  async logOut(jwt: string) {
    return await $fetch<BaseModel<object>>(`${this.apiBase}/auth`, {
      method: 'delete',
      headers: {
        Authorization: jwt,
      },
    })
  }
}

export default AuthApi
