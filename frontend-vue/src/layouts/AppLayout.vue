<template>
  <el-container class="layout">
    <el-header height="auto" class="header">
      <div class="header-inner">
        <div class="brand" @click="$router.push({ name: 'home' })">
          <span class="brand-icon">🖼️</span>
          <div>
            <span class="brand-name">Museu & Galeria</span>
            <span class="brand-sub">SDM · Projeto A3</span>
          </div>
        </div>

        <nav class="nav">
          <router-link v-for="link in links" :key="link.to" :to="link.to" class="nav-link">
            <span class="nav-icon">{{ link.icon }}</span>{{ link.label }}
          </router-link>
        </nav>

        <div class="header-user">
          <el-tag v-if="auth.canManage" size="small" type="warning" effect="plain">{{ auth.roleLabel }}</el-tag>
          <span class="user-name">{{ auth.user?.first_name }}</span>
          <el-button size="small" @click="logout">Sair</el-button>
        </div>
      </div>
    </el-header>

    <el-main class="layout-main">
      <div class="page">
        <router-view />
      </div>
    </el-main>

    <footer class="footer">
      Sistema de Gerenciamento de Museus e Galerias — trabalho acadêmico SDM 2026
    </footer>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const links = [
  { to: { name: 'home' }, label: 'Início', icon: '🏠' },
  { to: { name: 'galerias' }, label: 'Galerias', icon: '🏛️' },
  { to: { name: 'obras' }, label: 'Obras', icon: '🎨' },
  { to: { name: 'exposicoes' }, label: 'Exposições', icon: '📅' },
  { to: { name: 'perfil' }, label: 'Perfil', icon: '👤' },
]

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: var(--bg);
  flex-direction: column;
}

.header {
  background: #fff;
  border-bottom: 1px solid var(--border);
  padding: 0;
  height: auto !important;
}

.header-inner {
  max-width: 960px;
  margin: 0 auto;
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  user-select: none;
}

.brand-icon {
  font-size: 1.5rem;
}

.brand-name {
  display: block;
  font-weight: 700;
  font-size: 1rem;
  color: var(--text);
  line-height: 1.2;
}

.brand-sub {
  display: block;
  font-size: 0.7rem;
  color: var(--text-muted);
  font-weight: 400;
}

.nav {
  display: flex;
  gap: 0.25rem;
  flex: 1;
  flex-wrap: wrap;
}

.nav-link {
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-icon {
  font-size: 0.95rem;
}

.nav-link:hover {
  background: #f3f4f6;
  color: var(--text);
}

.nav-link.router-link-active {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-name {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.footer {
  text-align: center;
  padding: 1rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border);
  background: #fff;
}

@media (max-width: 640px) {
  .header-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .nav {
    width: 100%;
  }
}
</style>
