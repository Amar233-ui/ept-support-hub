/**
 * Minimal fetch wrapper for the backend API.
 * - cookies are always sent (auth is an HttpOnly JWT cookie, never stored in JS);
 * - the XSRF-TOKEN cookie is echoed in X-XSRF-TOKEN on mutating requests (Spring CSRF);
 * - errors are RFC 7807 ProblemDetail payloads.
 * Typed endpoints will be generated from the OpenAPI contract (src/api/schema.d.ts).
 */

export interface ProblemDetail {
  type?: string
  title?: string
  status: number
  detail?: string
  instance?: string
  [key: string]: unknown
}

export class ApiError extends Error {
  readonly problem: ProblemDetail

  constructor(problem: ProblemDetail) {
    super(problem.detail ?? problem.title ?? `HTTP ${problem.status}`)
    this.problem = problem
  }
}

const BASE_URL = '/api'
const SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

function readCookie(name: string): string | undefined {
  return document.cookie
    .split('; ')
    .find((c) => c.startsWith(`${name}=`))
    ?.split('=')[1]
}

export async function http<T>(path: string, init: RequestInit = {}): Promise<T> {
  const method = (init.method ?? 'GET').toUpperCase()
  const headers = new Headers(init.headers)
  headers.set('Accept', 'application/json')
  if (init.body && !(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (!SAFE_METHODS.includes(method)) {
    const xsrf = readCookie('XSRF-TOKEN')
    if (xsrf) headers.set('X-XSRF-TOKEN', decodeURIComponent(xsrf))
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...init, method, headers, credentials: 'include' })

  if (!response.ok) {
    const problem = await response
      .json()
      .catch(() => ({ status: response.status, title: response.statusText }) as ProblemDetail)
    throw new ApiError(problem as ProblemDetail)
  }
  return response.status === 204 ? (undefined as T) : ((await response.json()) as T)
}
