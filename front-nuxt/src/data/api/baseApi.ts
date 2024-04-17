class BaseAPI {
  protected apiBase: string

  constructor() {
    this.apiBase = useRuntimeConfig().public.apiBaseUrl
  }
}

export default BaseAPI
