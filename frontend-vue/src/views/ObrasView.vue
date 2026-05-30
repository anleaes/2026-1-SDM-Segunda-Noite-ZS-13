<template>
  <div v-loading="loading">
    <PageHeader
      theme="obras"
      icon="🎨"
      title="Obras de Arte"
      subtitle="Acervo catalogado por categoria e técnica"
    >
      <template v-if="auth.canManage" #extra>
        <el-button type="primary" @click="openCreate">+ Nova obra</el-button>
      </template>
    </PageHeader>

    <div class="filter-bar">
      <el-input v-model="search" placeholder="Buscar título ou técnica..." clearable style="max-width: 260px" @keyup.enter="load" />
      <el-select v-model="categoriaId" clearable placeholder="Categoria" style="width: 160px" @change="load">
        <el-option v-for="c in categorias" :key="c.id" :label="c.nome" :value="c.id" />
      </el-select>
      <el-button type="primary" @click="load">Buscar</el-button>
    </div>

    <div class="obra-grid">
      <article
        v-for="obra in obras"
        :key="obra.id"
        class="obra-card"
        @click="$router.push(`/obras/${obra.id}`)"
      >
        <div class="obra-thumb">{{ obra.titulo.charAt(0) }}</div>
        <div class="obra-body">
          <h3>{{ obra.titulo }}</h3>
          <p class="obra-meta">{{ obra.tecnica }} · {{ obra.ano_criacao }}</p>
          <p class="obra-valor">{{ formatMoney(obra.valor_estimado) }}</p>
        </div>
      </article>
    </div>

    <el-empty v-if="!loading && !obras.length" description="Nenhuma obra encontrada" />

    <el-dialog v-model="showForm" title="Nova obra de arte" width="520px" @closed="resetForm">
      <el-form label-position="top">
        <el-form-item label="Título" required>
          <el-input v-model="form.titulo" />
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="Técnica" required>
              <el-input v-model="form.tecnica" placeholder="Óleo sobre tela" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Ano" required>
              <el-input-number v-model="form.ano_criacao" :min="1000" :max="2100" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Valor estimado (R$)" required>
          <el-input-number v-model="form.valor_estimado" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Categoria" required>
          <div class="categoria-row">
            <el-select v-model="form.categoria" placeholder="Selecione" style="flex: 1">
              <el-option v-for="c in categorias" :key="c.id" :label="c.nome" :value="c.id" />
            </el-select>
            <el-button @click="showCatForm = true">+ Categoria</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvar">Criar obra</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showCatForm" title="Nova categoria" width="400px">
      <el-form label-position="top">
        <el-form-item label="Nome" required>
          <el-input v-model="catForm.nome" />
        </el-form-item>
        <el-form-item label="Descrição">
          <el-input v-model="catForm.descricao" type="textarea" rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCatForm = false">Cancelar</el-button>
        <el-button type="primary" :loading="savingCat" @click="salvarCategoria">Criar</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/PageHeader.vue'
import {
  apiError,
  createCategoria,
  createObra,
  fetchCategorias,
  fetchObras,
} from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const savingCat = ref(false)
const obras = ref([])
const categorias = ref([])
const search = ref('')
const categoriaId = ref(null)
const showForm = ref(false)
const showCatForm = ref(false)
const form = ref(emptyForm())
const catForm = ref({ nome: '', descricao: '' })

function emptyForm() {
  return {
    titulo: '',
    tecnica: '',
    ano_criacao: new Date().getFullYear(),
    valor_estimado: 0,
    categoria: null,
  }
}

function formatMoney(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function openCreate() {
  form.value = emptyForm()
  showForm.value = true
}

function resetForm() {
  form.value = emptyForm()
}

async function loadCategorias() {
  categorias.value = await fetchCategorias()
}

async function load() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (categoriaId.value) params.categoria = categoriaId.value
    obras.value = await fetchObras(Object.keys(params).length ? params : undefined)
  } finally {
    loading.value = false
  }
}

async function salvarCategoria() {
  if (!catForm.value.nome.trim()) {
    ElMessage.warning('Informe o nome da categoria.')
    return
  }
  savingCat.value = true
  try {
    const cat = await createCategoria(catForm.value)
    await loadCategorias()
    form.value.categoria = cat.id
    showCatForm.value = false
    catForm.value = { nome: '', descricao: '' }
    ElMessage.success('Categoria criada!')
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    savingCat.value = false
  }
}

async function salvar() {
  if (!form.value.titulo.trim() || !form.value.tecnica.trim() || !form.value.categoria) {
    ElMessage.warning('Preencha título, técnica e categoria.')
    return
  }
  saving.value = true
  try {
    const payload = {
      ...form.value,
      valor_estimado: String(form.value.valor_estimado),
    }
    const obra = await createObra(payload)
    ElMessage.success('Obra criada!')
    showForm.value = false
    router.push(`/obras/${obra.id}`)
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await loadCategorias()
  await load()
})
</script>

<style scoped>
.categoria-row {
  display: flex;
  gap: 0.5rem;
  width: 100%;
}

.obra-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.85rem;
}

.obra-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.15s;
}

.obra-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.obra-thumb {
  height: 88px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: #b45309;
}

.obra-body {
  padding: 0.85rem 1rem 1rem;
}

.obra-body h3 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.obra-meta {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.obra-valor {
  font-size: 0.9rem;
  font-weight: 600;
  color: #d97706;
  margin-top: 0.4rem;
}
</style>
