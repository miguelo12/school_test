import { Container } from 'inversify'

import AuthRepository from '@Data/repository/authRepository'
import type { authRepositoryInterface } from '@Data/repository/interface/authRepositoryInterface'
import { CONTAINER } from '@Domain/types/container'

const Singletons = new Container()
Singletons.bind<authRepositoryInterface>(CONTAINER.AuthRepository).to(AuthRepository)

export { Singletons }
