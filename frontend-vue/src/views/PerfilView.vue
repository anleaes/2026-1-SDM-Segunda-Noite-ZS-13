<template>
  <div v-loading="loading" class="perfil-page">
    <div class="profile-hero">
      <div class="avatar">{{ initials }}</div>
      <div class="profile-info">
        <h1>{{ auth.fullName || account?.username }}</h1>
        <el-tag effect="plain">{{ auth.roleLabel }}</el-tag>
        <p>@{{ account?.username }} · {{ account?.email }}</p>
      </div>
    </div>

    <el-tabs v-model="tab" class="profile-tabs">
      <el-tab-pane label="Dados da conta" name="dados">
        <el-form label-position="top" class="form-block">
          <div class="grid-2">
            <el-form-item label="Nome">
              <el-input v-model="form.first_name" />
            </el-form-item>
            <el-form-item label="Sobrenome">
              <el-input v-model="form.last_name" />
            </el-form-item>
          </div>
          <el-form-item label="E-mail">
            <el-input v-model="form.email" />
          </el-form-item>
          <el-form-item label="Telefone">
            <el-input v-model="form.telefone" />
          </el-form-item>
          <el-form-item label="Data de nascimento">
            <el-date-picker v-model="form.data_nascimento" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
          </el-form-item>

          <template v-if="account?.role === 'artista'">
            <el-form-item label="Nacionalidade">
              <el-input v-model="form.nacionalidade" />
            </el-form-item>
            <el-form-item label="Estilo artístico">
              <el-input v-model="form.estilo_artistico" />
            </el-form-item>
          </template>

          <el-descriptions :column="1" border style="margin-bottom: 1rem">
            <el-descriptions-item label="CPF">{{ account?.cpf }}</el-descriptions-item>
            <el-descriptions-item v-if="account?.data_cadastro" label="Data cadastro">
              {{ formatDate(account.data_cadastro) }}
            </el-descriptions-item>
            <el-descriptions-item v-if="account?.role === 'funcionario'" label="Cargo">
              {{ account.cargo }}
            </el-descriptions-item>
            <el-descriptions-item v-if="account?.role === 'funcionario'" label="Galeria">
              {{ account.galeria_nome || '—' }}
            </el-descriptions-item>
            <el-descriptions-item v-if="account?.role === 'funcionario'" label="Admissão">
              {{ formatDate(account.data_admissao) }}
            </el-descriptions-item>
          </el-descriptions>

          <el-button type="primary" :loading="saving" @click="salvarDados">Salvar alterações</el-button>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="Senha" name="senha">
        <el-form label-position="top" class="form-block narrow">
          <el-form-item label="Senha atual">
            <el-input v-model="pwd.current_password" type="password" show-password />
          </el-form-item>
          <el-form-item label="Nova senha">
            <el-input v-model="pwd.new_password" type="password" show-password />
          </el-form-item>
          <el-form-item label="Confirmar nova senha">
            <el-input v-model="pwd.new_password_confirm" type="password" show-password />
          </el-form-item>
          <el-button type="primary" :loading="savingPwd" @click="salvarSenha">Alterar senha</el-button>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="Minhas atividades" name="atividades">
        <template v-if="account?.role === 'visitante'">
          <el-card v-for="block in visitanteBlocks" :key="block.title" class="activity-card">
            <template #header>{{ block.title }} ({{ block.items.length }})</template>
            <el-empty v-if="!block.items.length" :description="block.empty" />
            <ul v-else class="list">
              <li v-for="item in block.items" :key="item.id">{{ block.format(item) }}</li>
            </ul>
          </el-card>
        </template>

        <template v-if="account?.role === 'funcionario'">
          <el-card class="activity-card">
            <template #header>Restaurações ({{ restauracoes.length }})</template>
            <el-empty v-if="!restauracoes.length" description="Nenhuma restauração" />
            <ul v-else class="list">
              <li v-for="r in restauracoes" :key="r.id">
                Obra #{{ r.obra }} · R$ {{ r.custo }} · {{ r.descricao }}
              </li>
            </ul>
          </el-card>
          <div class="info-box">Gerencie exposições na página de detalhe (alterar status).</div>
        </template>

        <template v-if="account?.role === 'artista'">
          <el-card class="activity-card">
            <template #header>Portfolio — ArtistaObra ({{ portfolio.length }})</template>
            <el-empty v-if="!portfolio.length" description="Nenhuma obra vinculada" />
            <ul v-else class="list">
              <li v-for="p in portfolio" :key="p.id">
                <router-link :to="`/obras/${p.obra.id}`">{{ p.obra.titulo }}</router-link>
                · {{ p.funcao }} · {{ formatDate(p.data_participacao) }}
              </li>
            </ul>
          </el-card>
        </template>
      </el-tab-pane>

      <el-tab-pane v-if="account?.role === 'visitante'" label="Excluir conta" name="excluir">
        <el-alert type="warning" show-icon :closable="false" title="Esta ação não pode ser desfeita." />
        <el-button type="danger" style="margin-top: 1rem" @click="confirmarExclusao">Excluir minha conta</el-button>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  apiError,
  changePassword,
  fetchAccount,
  fetchArtistaObras,
  fetchAvaliacoes,
  fetchIngressos,
  fetchObra,
  fetchPagamentos,
  fetchReservas,
  fetchRestauracoes,
} from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const savingPwd = ref(false)
const tab = ref('dados')
const account = ref(null)

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  telefone: '',
  data_nascimento: null,
  nacionalidade: '',
  estilo_artistico: '',
})

const pwd = reactive({
  current_password: '',
  new_password: '',
  new_password_confirm: '',
})

const ingressos = ref([])
const reservas = ref([])
const avaliacoes = ref([])
const pagamentos = ref([])
const restauracoes = ref([])
const portfolio = ref([])

const initials = computed(() => {
  const f = account.value?.first_name?.[0] || ''
  const l = account.value?.last_name?.[0] || ''
  return (f + l).toUpperCase() || '?'
})

const visitanteBlocks = computed(() => [
  {
    title: 'Ingressos',
    items: ingressos.value,
    empty: 'Nenhum ingresso',
    format: (i) => `Exposição #${i.exposicao} · ${i.tipo} · R$ ${i.valor} · ${i.status}`,
  },
  {
    title: 'Reservas',
    items: reservas.value,
    empty: 'Nenhuma reserva',
    format: (r) => `${formatDate(r.data_reserva)} · ${r.quantidade_pessoas} pessoas · ${r.status}`,
  },
  {
    title: 'Avaliações',
    items: avaliacoes.value,
    empty: 'Nenhuma avaliação',
    format: (a) => `${'★'.repeat(a.nota)} · ${a.comentario}`,
  },
  {
    title: 'Pagamentos',
    items: pagamentos.value,
    empty: 'Nenhum pagamento',
    format: (p) => `R$ ${p.valor} · ${p.metodo} · ${p.status} · ${formatDate(p.data_pagamento)}`,
  },
])

function formatDate(d) {
  if (!d) return '—'
  const [y, m, day] = String(d).split('-')
  return day ? `${day}/${m}/${y}` : d
}

function fillForm(data) {
  form.first_name = data.first_name || ''
  form.last_name = data.last_name || ''
  form.email = data.email || ''
  form.telefone = data.telefone || ''
  form.data_nascimento = data.data_nascimento || null
  form.nacionalidade = data.nacionalidade || ''
  form.estilo_artistico = data.estilo_artistico || ''
}

async function loadActivities(id, role) {
  if (role === 'visitante') {
    ;[ingressos.value, reservas.value, avaliacoes.value] = await Promise.all([
      fetchIngressos(id),
      fetchReservas(id),
      fetchAvaliacoes(id),
    ])
    const allPag = await fetchPagamentos()
    const ingIds = new Set(ingressos.value.map((i) => i.id))
    const resIds = new Set(reservas.value.map((r) => r.id))
    pagamentos.value = allPag.filter(
      (p) => (p.ingresso && ingIds.has(p.ingresso)) || (p.reserva && resIds.has(p.reserva)),
    )
  }
  if (role === 'funcionario') {
    restauracoes.value = await fetchRestauracoes(id)
  }
  if (role === 'artista') {
    const links = await fetchArtistaObras({ artista: id })
    portfolio.value = await Promise.all(
      links.map(async (link) => ({
        ...link,
        obra: await fetchObra(link.obra),
      })),
    )
  }
}

onMounted(async () => {
  const id = auth.user?.id
  if (!id) return
  try {
    account.value = await fetchAccount(id)
    fillForm(account.value)
    await loadActivities(id, account.value.role)
  } finally {
    loading.value = false
  }
})

async function salvarDados() {
  saving.value = true
  try {
    const payload = {
      first_name: form.first_name,
      last_name: form.last_name,
      email: form.email,
      telefone: form.telefone,
      data_nascimento: form.data_nascimento,
    }
    if (account.value?.role === 'artista') {
      payload.nacionalidade = form.nacionalidade
      payload.estilo_artistico = form.estilo_artistico
    }
    account.value = await auth.saveAccount(payload)
    ElMessage.success('Dados atualizados!')
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

async function salvarSenha() {
  savingPwd.value = true
  try {
    await changePassword(auth.user.id, { ...pwd })
    ElMessage.success('Senha alterada!')
    pwd.current_password = ''
    pwd.new_password = ''
    pwd.new_password_confirm = ''
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    savingPwd.value = false
  }
}

async function confirmarExclusao() {
  try {
    await ElMessageBox.confirm('Deseja realmente excluir sua conta de visitante?', 'Confirmar', {
      type: 'warning',
    })
    await auth.removeAccount()
    ElMessage.success('Conta excluída.')
    router.push({ name: 'login' })
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}
</script>

<style scoped>
.profile-hero {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.35rem;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 1.25rem;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #64748b, #94a3b8);
  color: #fff;
  font-weight: 700;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-info h1 {
  font-size: 1.25rem;
  margin-bottom: 0.35rem;
}

.profile-info p {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
}

.profile-tabs {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0 1rem 1rem;
}

.form-block {
  max-width: 520px;
}

.form-block.narrow {
  max-width: 360px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 1rem;
}

.activity-card {
  margin-bottom: 1rem;
}

@media (max-width: 520px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
