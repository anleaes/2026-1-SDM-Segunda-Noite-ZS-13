<template>
  <div v-loading="loading">
    <DetailBanner
      v-if="exposicao"
      variant="exposicao"
      :title="exposicao.titulo"
      :meta="`${formatDate(exposicao.data_inicio)} — ${formatDate(exposicao.data_fim)}`"
      :badge="statusLabel(exposicao.status)"
    >
      <template v-if="auth.canManage" #actions>
        <el-select v-model="novoStatus" size="small" style="width: 170px" @change="alterarStatus">
          <el-option label="Planejada" value="planejada" />
          <el-option label="Em andamento" value="em_andamento" />
          <el-option label="Encerrada" value="encerrada" />
        </el-select>
        <el-button size="small" @click="showEdit = true">Editar</el-button>
        <el-button size="small" type="danger" plain @click="confirmarExclusao">Excluir</el-button>
      </template>
    </DetailBanner>

    <div v-if="exposicao" class="split-layout">
      <div>
        <div class="content-panel" style="margin-bottom: 1rem">
          <p class="desc">{{ exposicao.descricao }}</p>
        </div>

        <div class="section-head">
          <h3 class="section-title">Obras expostas ({{ obrasExposicao.length }})</h3>
          <el-button v-if="auth.canManage" type="primary" size="small" @click="showAddObra = true">
            + Adicionar obra
          </el-button>
        </div>
        <div class="obra-exp-list">
          <div
            v-for="o in obrasExposicao"
            :key="o.link_id"
            class="obra-exp-row"
          >
            <div class="obra-exp-main" @click="goObra(o)">
              <div>
                <strong>{{ o.titulo }}</strong>
                <span>{{ o.tecnica }}</span>
              </div>
              <div class="obra-exp-meta">
                <span>Sala {{ o.posicao_sala }}</span>
                <el-tag size="small" effect="plain">{{ o.status_conservacao }}</el-tag>
              </div>
            </div>
            <el-button
              v-if="auth.canManage"
              type="danger"
              link
              size="small"
              @click.stop="removerObra(o)"
            >
              Remover
            </el-button>
          </div>
        </div>
        <el-empty v-if="!obrasExposicao.length" description="Nenhuma obra nesta exposição" />
      </div>

      <aside v-if="auth.user?.role === 'visitante'" class="sidebar-panel visitante-panel">
        <h3>🎟️ Área do visitante</h3>
        <p class="panel-hint">Ingresso, reserva e avaliação</p>

        <el-button type="primary" style="width: 100%; margin-bottom: 0.5rem" @click="showIngresso = true">
          Comprar ingressos
        </el-button>
        <el-button :loading="actionLoading" style="width: 100%; margin-bottom: 1rem" @click="showReserva = true">
          Reservar visita
        </el-button>

        <el-divider />

        <el-form label-position="top">
          <el-form-item label="Sua nota">
            <el-rate v-model="nota" :max="5" />
          </el-form-item>
          <el-form-item label="Comentário">
            <el-input v-model="comentario" type="textarea" rows="2" />
          </el-form-item>
          <el-button type="success" :loading="actionLoading" style="width: 100%" @click="avaliar">
            Enviar avaliação
          </el-button>
        </el-form>
      </aside>

      <aside v-else-if="auth.canManage" class="sidebar-panel func-panel">
        <h3>👔 Gestão da exposição</h3>
        <p class="panel-hint">
          Cadastre obras, altere o status e edite os dados da mostra. Como funcionário ou administrador,
          você gerencia todo o ciclo da exposição.
        </p>
        <ul class="staff-tips">
          <li>Adicione obras do acervo com posição na sala</li>
          <li>Altere o status para "Em andamento" ao abrir</li>
          <li>Encerre quando a mostra terminar</li>
        </ul>
      </aside>
    </div>

    <!-- Editar exposição -->
    <el-dialog v-model="showEdit" title="Editar exposição" width="520px">
      <el-form label-position="top">
        <el-form-item label="Título" required>
          <el-input v-model="editForm.titulo" />
        </el-form-item>
        <el-form-item label="Galeria" required>
          <el-select v-model="editForm.galeria" filterable style="width: 100%">
            <el-option v-for="g in galerias" :key="g.id" :label="g.nome" :value="g.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="Data início">
              <el-date-picker v-model="editForm.data_inicio" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Data fim">
              <el-date-picker v-model="editForm.data_fim" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Descrição">
          <el-input v-model="editForm.descricao" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEdit = false">Cancelar</el-button>
        <el-button type="primary" :loading="actionLoading" @click="salvarEdicao">Salvar</el-button>
      </template>
    </el-dialog>

    <!-- Adicionar obra -->
    <el-dialog v-model="showAddObra" title="Adicionar obra à exposição" width="520px">
      <el-form label-position="top">
        <el-form-item label="Obra" required>
          <el-select v-model="obraForm.obra" filterable placeholder="Selecione" style="width: 100%">
            <el-option v-for="o in obrasDisponiveis" :key="o.id" :label="o.titulo" :value="o.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Data de entrada" required>
          <el-date-picker v-model="obraForm.data_entrada" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Posição na sala" required>
          <el-input v-model="obraForm.posicao_sala" placeholder="Sala 2 - Parede norte" />
        </el-form-item>
        <el-form-item label="Status de conservação" required>
          <el-input v-model="obraForm.status_conservacao" placeholder="Ótimo, Bom, Regular..." />
        </el-form-item>
        <el-form-item label="Iluminação especial">
          <el-input v-model="obraForm.iluminacao_especial" />
        </el-form-item>
        <el-form-item label="Estilo da obra">
          <el-input v-model="obraForm.estilo_obra" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddObra = false">Cancelar</el-button>
        <el-button type="primary" :loading="actionLoading" @click="adicionarObra">Adicionar</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showIngresso" title="Comprar ingressos" width="400px">
      <el-form label-position="top">
        <el-form-item label="Quantidade de ingressos">
          <el-input-number v-model="ingressoQtd" :min="1" :max="20" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Tipo">
          <el-select v-model="ingressoTipo" style="width: 100%">
            <el-option label="Inteira — R$ 60" value="inteira" />
            <el-option label="Meia — R$ 30" value="meia" />
            <el-option label="Cortesia — R$ 0" value="cortesia" />
          </el-select>
        </el-form-item>
        <p class="total-line">
          Total: <strong>{{ formatMoney(ingressoQtd * INGRESSO_PRECOS[ingressoTipo]) }}</strong>
        </p>
        <p class="form-hint">
          Cada ingresso dá acesso à exposição inteira (todas as obras expostas). O sistema gera um bilhete por unidade.
        </p>
      </el-form>
      <template #footer>
        <el-button @click="showIngresso = false">Cancelar</el-button>
        <el-button type="primary" :loading="actionLoading" @click="comprar">Confirmar compra</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showReserva" title="Realizar reserva" width="360px">
      <el-form label-position="top">
        <el-form-item label="Quantidade de pessoas">
          <el-input-number v-model="reservaQtd" :min="1" :max="20" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Data">
          <el-date-picker v-model="reservaData" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showReserva = false">Cancelar</el-button>
        <el-button type="primary" :loading="actionLoading" @click="reservar">Confirmar</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import DetailBanner from '@/components/DetailBanner.vue'
import {
  apiError,
  comprarIngressos,
  INGRESSO_PRECOS,
  criarAvaliacao,
  criarReserva,
  deleteExposicao,
  deleteExposicaoObra,
  fetchExposicao,
  fetchExposicaoObras,
  fetchGalerias,
  fetchObra,
  fetchObras,
  updateExposicao,
  createExposicaoObra,
} from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const loading = ref(true)
const actionLoading = ref(false)
const exposicao = ref(null)
const obrasExposicao = ref([])
const galerias = ref([])
const todasObras = ref([])
const novoStatus = ref('')
const nota = ref(5)
const comentario = ref('Exposição excelente!')
const showReserva = ref(false)
const showIngresso = ref(false)
const showEdit = ref(false)
const showAddObra = ref(false)
const reservaQtd = ref(4)
const ingressoQtd = ref(1)
const ingressoTipo = ref('inteira')
const reservaData = ref('2026-08-15')
const editForm = ref({})
const obraForm = ref(emptyObraForm())

function emptyObraForm() {
  return {
    obra: null,
    data_entrada: '',
    posicao_sala: '',
    status_conservacao: 'Ótimo',
    iluminacao_especial: '',
    estilo_obra: '',
  }
}

const obrasDisponiveis = computed(() => {
  const ids = new Set(obrasExposicao.value.map((o) => o.obra_id))
  return todasObras.value.filter((o) => !ids.has(o.id))
})

const statusMap = {
  planejada: 'Planejada',
  em_andamento: 'Em andamento',
  encerrada: 'Encerrada',
}

function statusLabel(s) {
  return statusMap[s] || s
}

function formatDate(d) {
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

function formatMoney(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function goObra(row) {
  if (row.obra_id) router.push(`/obras/${row.obra_id}`)
}

watch(showEdit, (open) => {
  if (open && exposicao.value) {
    editForm.value = { ...exposicao.value }
  }
})

async function loadObrasExposicao() {
  const links = await fetchExposicaoObras(exposicao.value.id)
  obrasExposicao.value = await Promise.all(
    links.map(async (link) => {
      const obra = await fetchObra(link.obra)
      return {
        link_id: link.id,
        obra_id: link.obra,
        titulo: obra.titulo,
        tecnica: obra.tecnica,
        posicao_sala: link.posicao_sala,
        status_conservacao: link.status_conservacao,
      }
    }),
  )
}

onMounted(async () => {
  try {
    galerias.value = await fetchGalerias()
    todasObras.value = await fetchObras()
    exposicao.value = await fetchExposicao(route.params.id)
    novoStatus.value = exposicao.value.status
    await loadObrasExposicao()
  } finally {
    loading.value = false
  }
})

async function alterarStatus() {
  try {
    exposicao.value = await updateExposicao(exposicao.value.id, { status: novoStatus.value })
    ElMessage.success('Status atualizado!')
  } catch (e) {
    ElMessage.error(apiError(e))
    novoStatus.value = exposicao.value.status
  }
}

async function salvarEdicao() {
  actionLoading.value = true
  try {
    exposicao.value = await updateExposicao(exposicao.value.id, editForm.value)
    ElMessage.success('Exposição atualizada!')
    showEdit.value = false
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    actionLoading.value = false
  }
}

async function confirmarExclusao() {
  try {
    await ElMessageBox.confirm('Excluir esta exposição?', 'Confirmar exclusão', { type: 'warning' })
    await deleteExposicao(exposicao.value.id)
    ElMessage.success('Exposição excluída.')
    router.push({ name: 'exposicoes' })
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}

async function adicionarObra() {
  if (!obraForm.value.obra || !obraForm.value.data_entrada || !obraForm.value.posicao_sala) {
    ElMessage.warning('Preencha obra, data e posição na sala.')
    return
  }
  actionLoading.value = true
  try {
    await createExposicaoObra({
      exposicao: exposicao.value.id,
      ...obraForm.value,
    })
    await loadObrasExposicao()
    showAddObra.value = false
    obraForm.value = emptyObraForm()
    ElMessage.success('Obra adicionada à exposição!')
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    actionLoading.value = false
  }
}

async function removerObra(row) {
  try {
    await ElMessageBox.confirm(`Remover "${row.titulo}" desta exposição?`, 'Confirmar', { type: 'warning' })
    await deleteExposicaoObra(row.link_id)
    await loadObrasExposicao()
    ElMessage.success('Obra removida da exposição.')
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}

async function comprar() {
  actionLoading.value = true
  try {
    const criados = await comprarIngressos(
      auth.user.id,
      exposicao.value.id,
      ingressoQtd.value,
      ingressoTipo.value,
    )
    ElMessage.success(`${criados.length} ingresso(s) comprado(s)!`)
    showIngresso.value = false
    ingressoQtd.value = 1
    ingressoTipo.value = 'inteira'
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    actionLoading.value = false
  }
}

async function reservar() {
  actionLoading.value = true
  try {
    await criarReserva(auth.user.id, exposicao.value.id, reservaQtd.value, reservaData.value)
    ElMessage.success('Reserva confirmada!')
    showReserva.value = false
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    actionLoading.value = false
  }
}

async function avaliar() {
  actionLoading.value = true
  try {
    await criarAvaliacao(auth.user.id, exposicao.value.id, nota.value, comentario.value)
    ElMessage.success('Avaliação enviada!')
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    actionLoading.value = false
  }
}
</script>

<style scoped>
.desc {
  color: var(--text-muted);
  line-height: 1.65;
  font-size: 0.95rem;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.section-head .section-title {
  margin: 0;
}

.obra-exp-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.obra-exp-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1rem;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
}

.obra-exp-main {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}

.obra-exp-main:hover strong {
  color: #7c3aed;
}

.obra-exp-row span {
  display: block;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 0.15rem;
}

.obra-exp-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.visitante-panel {
  border-color: #bfdbfe;
  background: #f8fbff;
}

.func-panel {
  border-color: #bbf7d0;
  background: #f0fdf4;
}

.panel-hint {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.staff-tips {
  font-size: 0.82rem;
  color: var(--text-muted);
  padding-left: 1.1rem;
  line-height: 1.8;
}

.total-line {
  font-size: 0.95rem;
  margin: 0.5rem 0;
}

.form-hint {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.45;
}

@media (max-width: 768px) {
  .obra-exp-main {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
