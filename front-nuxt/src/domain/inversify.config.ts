import { Container } from 'inversify'

import AuthRepository from '../data/repository/authRepository'
import type { authRepositoryInterface } from '../data/repository/interface/authRepositoryInterface'
import { CONTAINER } from './types/container'

const Singletons = new Container()
Singletons.bind<authRepositoryInterface>(CONTAINER.AuthRepository).to(AuthRepository)

export { Singletons }
