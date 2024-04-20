import type { authLoginModel } from '@Data/model/authModel'
import type { BaseModel } from '@Data/model/baseModel'

export interface authRepositoryInterface {
  createUser(username: string, password: string): Promise<BaseModel<object>>
  logIn(username: string, password: string): Promise<BaseModel<authLoginModel>>
  logOut(jwt_token: string): Promise<BaseModel<object>>
}
