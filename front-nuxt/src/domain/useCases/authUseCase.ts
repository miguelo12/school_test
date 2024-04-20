import { injectable, inject } from 'inversify'
import type AuthRepository from '@Data/repository/authRepository'
import type { authLoginModel } from '@Data/model/authModel'
import { CONTAINER } from '@Domain/types/container'

@injectable()
class AuthUseCase {
  constructor(@inject(CONTAINER.AuthRepository) private authRepository: AuthRepository) {}

  async createUser(username: string, password: string): Promise<{ message: string, is_failed: boolean }> {
    let is_failed = false
    const { message } = await this.authRepository.createUser(username, password).catch(
      (err) => {
        is_failed = true
        return (err.data)
      },
    )
    return { message, is_failed }
  }

  async logIn(username: string, password: string): Promise<{ data: authLoginModel, message: string }> {
    return await this.authRepository.logIn(username, password).catch(
      err => err.data,
    )
  }

  async logOut(jwt_token: string): Promise<object> {
    return this.authRepository.logOut(jwt_token).catch(
      err => err.data,
    )
  }
}

export default AuthUseCase
