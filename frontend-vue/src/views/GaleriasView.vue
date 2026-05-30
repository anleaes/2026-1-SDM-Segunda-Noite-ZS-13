<template>
  <div v-loading="loading">
    <PageHeader
      theme="galerias"
      icon="🏛️"
      title="Galerias"
      subtitle="Museus e espaços expositivos"
    >
      <template #extra>
        <el-tag type="success" effect="plain">{{ abertas }} abertas</el-tag>
        <el-button v-if="auth.canManage" type="primary" @click="openCreate">
          + Nova galeria
        </el-button>
      </template>
    </PageHeader>

    <div class="filter-bar">
      <el-input
        v-model="search"
        placeholder="Buscar nome ou endereço..."
        clearable
        prefix-icon="Search"
        style="max-width: 280px"
        @input="load"
      />
      <el-radio-group v-model="filtroAberta" @change="load">
        <el-radio-button label="">Todas</el-radio-button>
        <el-radio-button label="true">Abertas</el-radio-button>
        <el-radio-button label="false">Fechadas</el-radio-button>
      </el-radio-group>
    </div>

    <div class="galeria-list">
      <article
        v-for="g in galerias"
        :key="g.id"
        class="galeria-row"
        @click="$router.push(`/galerias/${g.id}`)"
      >
        <div class="galeria-icon">{{ g.nome.charAt(0) }}</div>
        <div class="galeria-info">
          <div class="galeria-top">
            <h3>{{ g.nome }}</h3>
            <el-tag :type="g.aberta ? 'success' : 'info'" size="small" effect="plain">
              {{ g.aberta ? 'Aberta' : 'Fechada' }}
            </el-tag>
          </div>
          <p class="galeria-end">📍 {{ g.endereco }}</p>
          <p class="galeria-desc">{{ g.descricao }}</p>
        </div>
        <span class="galeria-arrow">›</span>
      </article>
    </div>

    <el-empty v-if="!loading && !galerias.length" description="Nenhuma galeria encontrada" />

    <el-dialog v-model="showForm" title="Nova galeria" width="480px" @closed="resetForm">
      <el-form label-position="top">
        <el-form-item label="Nome" required>
          <el-input v-model="form.nome" />
        </el-form-item>
        <el-form-item label="Endereço" required>
          <el-input v-model="form.endereco" />
        </el-form-item>
        <el-form-item label="Descrição">
          <el-input v-model="form.descricao" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="Status">
          <el-switch v-model="form.aberta" active-text="Aberta" inactive-text="Fechada" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvar">Criar galeria</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/PageHeader.vue'
import { apiError, createGaleria, fetchGalerias } from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const galerias = ref([])
const allGalerias = ref([])
const search = ref('')
const filtroAberta = ref('')
const showForm = ref(false)
const form = ref(emptyForm())

function emptyForm() {
  return { nome: '', endereco: '', descricao: '', aberta: true }
}

const abertas = computed(() => allGalerias.value.filter((g) => g.aberta).length)

function openCreate() {
  form.value = emptyForm()
  showForm.value = true
}

function resetForm() {
  form.value = emptyForm()
}

async function load() {
  loading.value = true
  try {
    const params = {}
    if (filtroAberta.value !== '') params.aberta = filtroAberta.value
    allGalerias.value = await fetchGalerias(params)
    galerias.value = allGalerias.value
    if (search.value) {
      const q = search.value.toLowerCase()
      galerias.value = galerias.value.filter(
        (g) => g.nome.toLowerCase().includes(q) || g.endereco.toLowerCase().includes(q),
      )
    }
  } finally {
    loading.value = false
  }
}

async function salvar() {
  if (!form.value.nome.trim() || !form.value.endereco.trim()) {
    ElMessage.warning('Preencha nome e endereço.')
    return
  }
  saving.value = true
  try {
    const g = await createGaleria(form.value)
    ElMessage.success('Galeria criada!')
    showForm.value = false
    router.push(`/galerias/${g.id}`)
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.galeria-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.galeria-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.15rem;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.galeria-row:hover {
  border-color: #10b981;
  box-shadow: var(--shadow);
}

.galeria-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: #ecfdf5;
  color: #059669;
  font-weight: 700;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.galeria-info {
  flex: 1;
  min-width: 0;
}

.galeria-top {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.galeria-top h3 {
  font-size: 1rem;
  font-weight: 600;
}

.galeria-end {
  font-size: 0.82rem;
  color: #059669;
  margin-top: 0.2rem;
}

.galeria-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.galeria-arrow {
  font-size: 1.5rem;
  color: var(--text-muted);
  flex-shrink: 0;
}
</style>
