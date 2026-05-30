<template>
  <div v-loading="loading">
    <PageHeader
      theme="exposicoes"
      icon="📅"
      title="Exposições"
      subtitle="Mostras em cartaz, planejadas e encerradas"
    >
      <template v-if="auth.canManage" #extra>
        <el-button type="primary" @click="openCreate">+ Nova exposição</el-button>
      </template>
    </PageHeader>

    <div class="filter-bar">
      <span class="filter-label">Status:</span>
      <el-radio-group v-model="statusFilter" @change="load">
        <el-radio-button label="">Todas</el-radio-button>
        <el-radio-button label="planejada">Planejada</el-radio-button>
        <el-radio-button label="em_andamento">Em andamento</el-radio-button>
        <el-radio-button label="encerrada">Encerrada</el-radio-button>
      </el-radio-group>
    </div>

    <div class="timeline">
      <article
        v-for="e in exposicoes"
        :key="e.id"
        class="timeline-item"
        @click="$router.push(`/exposicoes/${e.id}`)"
      >
        <div class="timeline-dot" :class="`dot-${e.status}`" />
        <div class="timeline-card">
          <div class="timeline-head">
            <h3>{{ e.titulo }}</h3>
            <el-tag size="small" :type="tagType(e.status)" effect="plain">
              {{ statusLabel(e.status) }}
            </el-tag>
          </div>
          <p class="timeline-date">{{ formatDate(e.data_inicio) }} — {{ formatDate(e.data_fim) }}</p>
          <p class="timeline-desc">{{ e.descricao }}</p>
        </div>
      </article>
    </div>

    <el-empty v-if="!loading && !exposicoes.length" description="Nenhuma exposição encontrada" />

    <el-dialog v-model="showForm" title="Nova exposição" width="520px" @closed="resetForm">
      <el-form label-position="top">
        <el-form-item label="Título" required>
          <el-input v-model="form.titulo" />
        </el-form-item>
        <el-form-item label="Galeria" required>
          <el-select v-model="form.galeria" filterable placeholder="Selecione a galeria" style="width: 100%">
            <el-option v-for="g in galerias" :key="g.id" :label="g.nome" :value="g.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="Data início" required>
              <el-date-picker v-model="form.data_inicio" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Data fim" required>
              <el-date-picker v-model="form.data_fim" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="Planejada" value="planejada" />
            <el-option label="Em andamento" value="em_andamento" />
            <el-option label="Encerrada" value="encerrada" />
          </el-select>
        </el-form-item>
        <el-form-item label="Descrição">
          <el-input v-model="form.descricao" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvar">Criar exposição</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/PageHeader.vue'
import { apiError, createExposicao, fetchExposicoes, fetchGalerias } from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const exposicoes = ref([])
const galerias = ref([])
const statusFilter = ref('')
const showForm = ref(false)
const form = ref(emptyForm())

function emptyForm() {
  return {
    titulo: '',
    descricao: '',
    data_inicio: '',
    data_fim: '',
    status: 'planejada',
    galeria: null,
  }
}

const statusMap = {
  planejada: 'Planejada',
  em_andamento: 'Em andamento',
  encerrada: 'Encerrada',
}

function statusLabel(s) {
  return statusMap[s] || s
}

function tagType(s) {
  if (s === 'em_andamento') return 'success'
  if (s === 'encerrada') return 'info'
  return 'warning'
}

function formatDate(d) {
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

function openCreate() {
  form.value = emptyForm()
  if (route.query.galeria) {
    form.value.galeria = Number(route.query.galeria)
  }
  showForm.value = true
}

function resetForm() {
  form.value = emptyForm()
}

async function load() {
  loading.value = true
  try {
    const params = statusFilter.value ? { status: statusFilter.value } : undefined
    exposicoes.value = await fetchExposicoes(params)
  } finally {
    loading.value = false
  }
}

async function salvar() {
  if (!form.value.titulo.trim() || !form.value.galeria || !form.value.data_inicio || !form.value.data_fim) {
    ElMessage.warning('Preencha título, galeria e datas.')
    return
  }
  saving.value = true
  try {
    const exp = await createExposicao(form.value)
    ElMessage.success('Exposição criada!')
    showForm.value = false
    router.push(`/exposicoes/${exp.id}`)
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  galerias.value = await fetchGalerias()
  await load()
  if (route.query.nova === '1' && auth.canManage) {
    openCreate()
  }
})
</script>

<style scoped>
.filter-label {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: #e9d5ff;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
}

.timeline-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 1rem;
  margin-left: -1.5rem;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #e9d5ff;
}

.dot-planejada { background: #f59e0b; }
.dot-em_andamento { background: #10b981; }
.dot-encerrada { background: #9ca3af; }

.timeline-card {
  flex: 1;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.15rem;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.timeline-item:hover .timeline-card {
  border-color: #c084fc;
  box-shadow: var(--shadow);
}

.timeline-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.timeline-head h3 {
  font-size: 1rem;
  font-weight: 600;
}

.timeline-date {
  font-size: 0.82rem;
  color: #7c3aed;
  margin: 0.35rem 0;
}

.timeline-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.5;
}
</style>
