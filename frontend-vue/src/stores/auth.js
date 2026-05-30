import { defineStore } from 'pinia'
import {
  deleteAccount as apiDeleteAccount,
  fetchAccount,
  loginUser,
  registerUser,
  updateAccount,
} from '@/api/services'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('museu_user') || 'null'),
  }),
  getters: {
    isLoggedIn: (state) => !!state.user,
    fullName: (state) =>
      state.user ? `${state.user.first_name} ${state.user.last_name}`.trim() : '',
    roleLabel: (state) => {
      const map = {
        visitante: 'Visitante',
        funcionario: 'Funcionário',
        artista: 'Artista',
        admin: 'Administrador',
        usuario: 'Usuário',
      }
      return state.user ? map[state.user.role] || state.user.role : ''
    },
    canManage: (state) =>
      state.user?.role === 'funcionario' || state.user?.role === 'admin',
  },
  actions: {
    _persist(user) {
      this.user = user
      localStorage.setItem('museu_user', JSON.stringify(user))
    },
    async login(username, password) {
      const user = await loginUser(username, password)
      this._persist(user)
    },
    async register(payload) {
      const user = await registerUser(payload)
      this._persist(user)
    },
    async refreshAccount() {
      if (!this.user?.id) return
      const user = await fetchAccount(this.user.id)
      this._persist(user)
    },
    async saveAccount(payload) {
      const user = await updateAccount(this.user.id, payload)
      this._persist(user)
      return user
    },
    async removeAccount() {
      await apiDeleteAccount(this.user.id)
      this.logout()
    },
    logout() {
      this.user = null
      localStorage.removeItem('museu_user')
    },
  },
})
