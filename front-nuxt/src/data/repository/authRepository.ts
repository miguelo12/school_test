import { injectable } from 'inversify'
import AuthApi from '@Data/api/authApi'
import type { authLoginModel } from '@Data/model/authModel'
import type { BaseModel } from '@Data/model/baseModel'
import type { authRepositoryInterface } from '@Data/repository/interface/authRepositoryInterface'

@injectable()
class AuthRepository implements authRepositoryInterface {
  private authApi: AuthApi
  constructor() {
    this.authApi = new AuthApi()
  }

  async createUser(username: string, password: string): Promise<BaseModel<object>> {
    return this.authApi.CreateUser(username, password)
  }

  async logIn(username: string, password: string): Promise<BaseModel<authLoginModel>> {
    return this.authApi.logIn(username, password)
  }

  async logOut(jwt_token: string): Promise<BaseModel<object>> {
    return this.authApi.logOut(jwt_token)
  }
}

export default AuthRepository
