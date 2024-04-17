import type { authLoginModel } from '../../model/authModel'
import type { BaseModel } from '../../model/baseModel'

export interface authRepositoryInterface {
  createUser(username: string, password: string): Promise<BaseModel<object>>
  logIn(username: string, password: string): Promise<BaseModel<authLoginModel>>
  logOut(jwt_token: string): Promise<BaseModel<object>>
}
