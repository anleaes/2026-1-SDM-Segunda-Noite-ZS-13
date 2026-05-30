<template>
  <div v-loading="loading">
    <DetailBanner
      v-if="galeria"
      variant="galeria"
      :title="galeria.nome"
      :meta="galeria.endereco"
      :badge="galeria.aberta ? 'Aberta ao público' : 'Fechada'"
    >
      <template v-if="auth.canManage" #actions>
        <el-button size="small" @click="showEdit = true">Editar</el-button>
        <el-button size="small" type="danger" plain @click="confirmarExclusao">Excluir</el-button>
      </template>
    </DetailBanner>

    <template v-if="galeria">
      <div class="content-panel" style="margin-bottom: 1.25rem">
        <p class="desc">{{ galeria.descricao }}</p>
      </div>

      <div class="section-head">
        <h3 class="section-title">Exposições nesta galeria ({{ exposicoes.length }})</h3>
        <el-button v-if="auth.canManage" type="primary" size="small" @click="novaExposicao">
          + Nova exposição
        </el-button>
      </div>
      <div class="exp-mini-list">
        <div
          v-for="e in exposicoes"
          :key="e.id"
          class="exp-mini-item"
          @click="$router.push(`/exposicoes/${e.id}`)"
        >
          <span class="exp-mini-title">{{ e.titulo }}</span>
          <el-tag size="small" effect="plain">{{ e.status }}</el-tag>
          <span class="exp-mini-date">{{ e.data_inicio }} → {{ e.data_fim }}</span>
        </div>
      </div>
      <el-empty v-if="!exposicoes.length" description="Sem exposições nesta galeria" />
    </template>

    <el-dialog v-model="showEdit" title="Editar galeria" width="480px">
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
        <el-button @click="showEdit = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvar">Salvar</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import DetailBanner from '@/components/DetailBanner.vue'
import {
  apiError,
  deleteGaleria,
  fetchExposicoes,
  fetchGaleria,
  updateGaleria,
} from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const galeria = ref(null)
const exposicoes = ref([])
const showEdit = ref(false)
const form = ref({})

watch(showEdit, (open) => {
  if (open && galeria.value) {
    form.value = { ...galeria.value }
  }
})

async function load() {
  const id = route.params.id
  loading.value = true
  try {
    galeria.value = await fetchGaleria(id)
    exposicoes.value = await fetchExposicoes({ galeria: id })
  } finally {
    loading.value = false
  }
}

async function salvar() {
  saving.value = true
  try {
    galeria.value = await updateGaleria(galeria.value.id, form.value)
    ElMessage.success('Galeria atualizada!')
    showEdit.value = false
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

async function confirmarExclusao() {
  try {
    await ElMessageBox.confirm(
      'Excluir esta galeria? Exposições vinculadas também serão removidas.',
      'Confirmar exclusão',
      { type: 'warning' },
    )
    await deleteGaleria(galeria.value.id)
    ElMessage.success('Galeria excluída.')
    router.push({ name: 'galerias' })
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}

function novaExposicao() {
  router.push({ name: 'exposicoes', query: { nova: 1, galeria: galeria.value.id } })
}

onMounted(load)
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
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.section-head .section-title {
  margin: 0;
}

.exp-mini-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.exp-mini-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 0.75rem;
  align-items: center;
  padding: 0.85rem 1rem;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
}

.exp-mini-item:hover {
  border-color: #10b981;
}

.exp-mini-title {
  font-weight: 600;
  font-size: 0.9rem;
}

.exp-mini-date {
  font-size: 0.78rem;
  color: var(--text-muted);
}

@media (max-width: 560px) {
  .exp-mini-item {
    grid-template-columns: 1fr;
  }
}
</style>
