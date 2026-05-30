<template>
  <div class="login-page">
    <div class="login-wrap">
      <div class="login-side">
        <span class="login-emoji">🏛️</span>
        <h2>Museu & Galeria</h2>
        <p>Sistema de gerenciamento para museus e galerias de arte.</p>
        <ul class="login-features">
          <li>Consultar galerias e obras</li>
          <li>Ver exposições em cartaz</li>
          <li>Comprar ingressos e reservar visitas</li>
        </ul>
      </div>

      <el-card class="login-card" shadow="never">
        <h1>Entrar</h1>
        <p class="login-sub">Use seu usuário e senha do sistema</p>

        <el-form @submit.prevent="handleLogin" label-position="top">
          <el-form-item label="Usuário">
            <el-input v-model="username" placeholder="Seu usuário" size="large" autocomplete="username" />
          </el-form-item>

          <el-form-item label="Senha">
            <el-input
              v-model="password"
              type="password"
              placeholder="Sua senha"
              show-password
              size="large"
              autocomplete="current-password"
            />
          </el-form-item>

          <el-button type="primary" native-type="submit" :loading="loading" size="large" style="width: 100%; margin-top: 0.5rem">
            Entrar
          </el-button>
        </el-form>

        <p class="register-link">
          Não tem conta? <router-link :to="{ name: 'register' }">Cadastre-se como visitante</router-link>
        </p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!username.value.trim() || !password.value) {
    ElMessage.warning('Informe usuário e senha.')
    return
  }
  loading.value = true
  try {
    await auth.login(username.value.trim(), password.value)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    router.push(redirect)
  } catch (e) {
    const status = e.response?.status
    let msg = e.response?.data?.detail || e.message || 'Erro ao entrar.'
    if (status === 403) {
      msg = 'Acesso negado (403). Reinicie o backend Django após atualizar o projeto.'
    } else if (!e.response) {
      msg = 'Backend inacessível. Rode: python manage.py runserver 0.0.0.0:8000'
    }
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: var(--bg);
}

.login-wrap {
  display: flex;
  gap: 2rem;
  max-width: 820px;
  width: 100%;
  align-items: stretch;
}

.login-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem;
}

.login-emoji {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.login-side h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.login-side > p {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin-bottom: 1.25rem;
}

.login-features {
  list-style: none;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.login-features li {
  padding: 0.35rem 0;
  padding-left: 1.25rem;
  position: relative;
}

.login-features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-weight: 600;
}

.login-card {
  flex: 1;
  max-width: 380px;
  padding: 0.5rem;
}

.login-card h1 {
  font-size: 1.35rem;
  margin-bottom: 0.25rem;
}

.login-sub {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}

@media (max-width: 700px) {
  .login-wrap {
    flex-direction: column;
  }

  .login-side {
    text-align: center;
    padding: 0;
  }

  .login-features {
    display: none;
  }

  .login-card {
    max-width: 100%;
  }
}
</style>
