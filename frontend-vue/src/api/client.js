import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { Accept: 'application/json' },
})

export default api

export function unwrap(data) {
  return data.results ?? data
}
