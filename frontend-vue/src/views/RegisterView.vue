<template>
  <div class="register-page">
    <el-card class="register-card" shadow="never">
      <h1>Criar conta</h1>
      <p class="sub">Cadastro público para visitantes do museu</p>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleRegister">
        <div class="grid-2">
          <el-form-item label="Nome" prop="first_name">
            <el-input v-model="form.first_name" />
          </el-form-item>
          <el-form-item label="Sobrenome" prop="last_name">
            <el-input v-model="form.last_name" />
          </el-form-item>
        </div>

        <el-form-item label="Usuário (login)" prop="username">
          <el-input v-model="form.username" placeholder="maria.silva" />
        </el-form-item>

        <el-form-item label="E-mail" prop="email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>

        <el-form-item label="CPF" prop="cpf">
          <el-input v-model="form.cpf" placeholder="12345678901" maxlength="14" />
        </el-form-item>

        <el-form-item label="Telefone" prop="telefone">
          <el-input v-model="form.telefone" placeholder="(11) 99999-9999" />
        </el-form-item>

        <el-form-item label="Data de nascimento">
          <el-date-picker
            v-model="form.data_nascimento"
            type="date"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <div class="grid-2">
          <el-form-item label="Senha" prop="password">
            <el-input v-model="form.password" type="password" show-password />
          </el-form-item>
          <el-form-item label="Confirmar senha" prop="password_confirm">
            <el-input v-model="form.password_confirm" type="password" show-password />
          </el-form-item>
        </div>

        <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%">
          Cadastrar
        </el-button>
      </el-form>

      <p class="login-link">
        Já tem conta?
        <router-link :to="{ name: 'login' }">Entrar</router-link>
      </p>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { apiError } from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  password_confirm: '',
  email: '',
  first_name: '',
  last_name: '',
  cpf: '',
  telefone: '',
  data_nascimento: null,
})

const rules = {
  username: [{ required: true, message: 'Informe o usuário' }],
  first_name: [{ required: true, message: 'Informe o nome' }],
  last_name: [{ required: true, message: 'Informe o sobrenome' }],
  email: [{ required: true, type: 'email', message: 'E-mail inválido' }],
  cpf: [{ required: true, min: 11, message: 'CPF obrigatório' }],
  password: [{ required: true, min: 6, message: 'Mínimo 6 caracteres' }],
  password_confirm: [{ required: true, message: 'Confirme a senha' }],
}

async function handleRegister() {
  await formRef.value.validate()
  loading.value = true
  try {
    const payload = { ...form }
    if (!payload.data_nascimento) delete payload.data_nascimento
    await auth.register(payload)
    ElMessage.success('Conta criada com sucesso!')
    router.push({ name: 'home' })
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem 1rem;
  background: var(--bg);
}

.register-card {
  width: 100%;
  max-width: 520px;
}

.register-card h1 {
  font-size: 1.35rem;
  margin-bottom: 0.25rem;
}

.sub {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 1rem;
}

.login-link {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.9rem;
  color: var(--text-muted);
}

@media (max-width: 520px) {
  .grid-2 {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
