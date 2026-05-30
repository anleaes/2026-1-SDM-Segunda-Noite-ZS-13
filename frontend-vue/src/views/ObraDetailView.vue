<template>
  <div v-loading="loading">
    <DetailBanner
      v-if="obra"
      variant="obra"
      :title="obra.titulo"
      :meta="`${obra.tecnica} · ${obra.ano_criacao}`"
      :badge="categoria?.nome"
    >
      <template v-if="auth.canManage" #actions>
        <el-button size="small" @click="showEdit = true">Editar</el-button>
        <el-button size="small" type="danger" plain @click="confirmarExclusao">Excluir</el-button>
      </template>
    </DetailBanner>

    <template v-if="obra">
      <div class="obra-layout">
        <div class="content-panel">
          <p class="price">{{ formatMoney(obra.valor_estimado) }}</p>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="Técnica">{{ obra.tecnica }}</el-descriptions-item>
            <el-descriptions-item label="Ano">{{ obra.ano_criacao }}</el-descriptions-item>
            <el-descriptions-item label="Categoria">{{ categoria?.nome || '—' }}</el-descriptions-item>
          </el-descriptions>

          <div class="section-head">
            <h3 class="section-title">Artistas</h3>
            <el-button v-if="auth.canManage" size="small" type="primary" plain @click="showArtista = true">
              + Vincular artista
            </el-button>
          </div>
          <ul v-if="artistas.length" class="artist-chips">
            <li v-for="a in artistas" :key="a.id">
              <div class="artist-row">
                <div>
                  <strong>{{ a.artista_nome }}</strong>
                  <span>{{ a.funcao }} · {{ formatDate(a.data_participacao) }}</span>
                </div>
                <el-button
                  v-if="auth.canManage"
                  type="danger"
                  link
                  size="small"
                  @click="removerArtista(a)"
                >
                  Remover
                </el-button>
              </div>
            </li>
          </ul>
          <p v-else class="empty-hint">Nenhum artista vinculado.</p>
        </div>

        <aside class="side-stack">
          <div v-if="certificado" class="cert-panel">
            <div class="panel-head">
              <h3>🪪 Certificado</h3>
              <el-button v-if="auth.canManage" link size="small" @click="editarCertificado">Editar</el-button>
            </div>
            <p><span>Código</span>{{ certificado.codigo }}</p>
            <p><span>Emissão</span>{{ formatDate(certificado.data_emissao) }}</p>
            <p><span>Órgão</span>{{ certificado.orgao_responsavel }}</p>
            <el-tag v-if="certificadoValido" type="success" size="small">Válido</el-tag>
          </div>
          <div v-else-if="auth.canManage" class="cert-panel cert-empty">
            <h3>🪪 Certificado</h3>
            <p class="empty-hint">Obra sem certificado de autenticidade.</p>
            <el-button type="primary" size="small" @click="showCert = true">Emitir certificado</el-button>
          </div>

          <div v-if="auth.user?.role === 'funcionario'" class="staff-panel">
            <h3>🔧 Restauração</h3>
            <p class="empty-hint">Registrar intervenção de conservação nesta obra.</p>
            <el-button size="small" @click="showRestauracao = true">Registrar restauração</el-button>
          </div>
        </aside>
      </div>
    </template>

    <!-- Editar obra -->
    <el-dialog v-model="showEdit" title="Editar obra" width="520px">
      <el-form label-position="top">
        <el-form-item label="Título" required>
          <el-input v-model="form.titulo" />
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="Técnica">
              <el-input v-model="form.tecnica" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Ano">
              <el-input-number v-model="form.ano_criacao" :min="1000" :max="2100" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Valor estimado (R$)">
          <el-input-number v-model="form.valor_estimado" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Categoria">
          <el-select v-model="form.categoria" style="width: 100%">
            <el-option v-for="c in categorias" :key="c.id" :label="c.nome" :value="c.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEdit = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvarObra">Salvar</el-button>
      </template>
    </el-dialog>

    <!-- Certificado -->
    <el-dialog v-model="showCert" :title="certificado ? 'Editar certificado' : 'Emitir certificado'" width="440px">
      <el-form label-position="top">
        <el-form-item label="Código" required>
          <el-input v-model="certForm.codigo" />
        </el-form-item>
        <el-form-item label="Data de emissão" required>
          <el-date-picker v-model="certForm.data_emissao" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Órgão responsável" required>
          <el-input v-model="certForm.orgao_responsavel" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCert = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvarCertificado">Salvar</el-button>
      </template>
    </el-dialog>

    <!-- Artista -->
    <el-dialog v-model="showArtista" title="Vincular artista" width="440px">
      <el-form label-position="top">
        <el-form-item label="Artista" required>
          <el-select v-model="artistaForm.artista" filterable placeholder="Selecione" style="width: 100%">
            <el-option
              v-for="a in artistasLista"
              :key="a.id"
              :label="`${a.first_name} ${a.last_name}`.trim() || a.username"
              :value="a.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Função" required>
          <el-input v-model="artistaForm.funcao" placeholder="Autor, coautor..." />
        </el-form-item>
        <el-form-item label="Data de participação" required>
          <el-date-picker
            v-model="artistaForm.data_participacao"
            type="date"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showArtista = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="vincularArtista">Vincular</el-button>
      </template>
    </el-dialog>

    <!-- Restauração -->
    <el-dialog v-model="showRestauracao" title="Registrar restauração" width="440px">
      <el-form label-position="top">
        <el-form-item label="Data de início" required>
          <el-date-picker v-model="restForm.data_inicio" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Descrição" required>
          <el-input v-model="restForm.descricao" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="Custo (R$)" required>
          <el-input-number v-model="restForm.custo" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRestauracao = false">Cancelar</el-button>
        <el-button type="primary" :loading="saving" @click="salvarRestauracao">Registrar</el-button>
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
  createArtistaObra,
  createCertificado,
  createRestauracao,
  deleteArtistaObra,
  deleteObra,
  fetchArtista,
  fetchArtistaObras,
  fetchArtistas,
  fetchCategorias,
  fetchCategoria,
  fetchCertificados,
  fetchObra,
  updateCertificado,
  updateObra,
} from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const obra = ref(null)
const categoria = ref(null)
const categorias = ref([])
const certificado = ref(null)
const artistas = ref([])
const artistasLista = ref([])
const showEdit = ref(false)
const showCert = ref(false)
const showArtista = ref(false)
const showRestauracao = ref(false)
const form = ref({})
const certForm = ref(emptyCert())
const artistaForm = ref({ artista: null, funcao: 'Autor', data_participacao: '' })
const restForm = ref({ data_inicio: '', descricao: '', custo: 0 })

const certificadoValido = computed(() => certificado.value?.codigo && certificado.value?.data_emissao)

function emptyCert() {
  return { codigo: '', data_emissao: '', orgao_responsavel: '' }
}

function formatMoney(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
function formatDate(d) {
  if (!d) return '—'
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

watch(showEdit, (open) => {
  if (open && obra.value) {
    form.value = {
      ...obra.value,
      valor_estimado: Number(obra.value.valor_estimado),
    }
  }
})

async function loadArtistas() {
  const links = await fetchArtistaObras({ obra: obra.value.id })
  artistas.value = await Promise.all(
    links.map(async (l) => {
      const a = await fetchArtista(l.artista)
      return {
        ...l,
        artista_nome: `${a.first_name} ${a.last_name}`.trim() || a.username,
      }
    }),
  )
}

async function load() {
  try {
    obra.value = await fetchObra(route.params.id)
    categorias.value = await fetchCategorias()
    if (obra.value.categoria) {
      categoria.value = await fetchCategoria(obra.value.categoria)
    }
    const certs = await fetchCertificados(obra.value.id)
    certificado.value = certs[0] || null
    artistasLista.value = await fetchArtistas()
    await loadArtistas()
  } finally {
    loading.value = false
  }
}

async function salvarObra() {
  saving.value = true
  try {
    const payload = { ...form.value, valor_estimado: String(form.value.valor_estimado) }
    obra.value = await updateObra(obra.value.id, payload)
    if (obra.value.categoria) {
      categoria.value = await fetchCategoria(obra.value.categoria)
    }
    ElMessage.success('Obra atualizada!')
    showEdit.value = false
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

async function confirmarExclusao() {
  try {
    await ElMessageBox.confirm('Excluir esta obra permanentemente?', 'Confirmar exclusão', { type: 'warning' })
    await deleteObra(obra.value.id)
    ElMessage.success('Obra excluída.')
    router.push({ name: 'obras' })
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}

function editarCertificado() {
  certForm.value = certificado.value ? { ...certificado.value } : emptyCert()
  showCert.value = true
}

async function salvarCertificado() {
  if (!certForm.value.codigo || !certForm.value.data_emissao || !certForm.value.orgao_responsavel) {
    ElMessage.warning('Preencha todos os campos do certificado.')
    return
  }
  saving.value = true
  try {
    if (certificado.value) {
      certificado.value = await updateCertificado(certificado.value.id, certForm.value)
    } else {
      certificado.value = await createCertificado({ ...certForm.value, obra: obra.value.id })
    }
    ElMessage.success('Certificado salvo!')
    showCert.value = false
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

async function vincularArtista() {
  if (!artistaForm.value.artista || !artistaForm.value.funcao || !artistaForm.value.data_participacao) {
    ElMessage.warning('Preencha artista, função e data.')
    return
  }
  saving.value = true
  try {
    await createArtistaObra({
      artista: artistaForm.value.artista,
      obra: obra.value.id,
      funcao: artistaForm.value.funcao,
      data_participacao: artistaForm.value.data_participacao,
    })
    await loadArtistas()
    showArtista.value = false
    artistaForm.value = { artista: null, funcao: 'Autor', data_participacao: '' }
    ElMessage.success('Artista vinculado!')
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

async function removerArtista(link) {
  try {
    await ElMessageBox.confirm('Remover vínculo com este artista?', 'Confirmar', { type: 'warning' })
    await deleteArtistaObra(link.id)
    await loadArtistas()
    ElMessage.success('Vínculo removido.')
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(apiError(e))
  }
}

async function salvarRestauracao() {
  if (!restForm.value.data_inicio || !restForm.value.descricao) {
    ElMessage.warning('Preencha data e descrição.')
    return
  }
  saving.value = true
  try {
    await createRestauracao({
      obra: obra.value.id,
      funcionario: auth.user.id,
      data_inicio: restForm.value.data_inicio,
      descricao: restForm.value.descricao,
      custo: String(restForm.value.custo),
    })
    ElMessage.success('Restauração registrada!')
    showRestauracao.value = false
    restForm.value = { data_inicio: '', descricao: '', custo: 0 }
  } catch (e) {
    ElMessage.error(apiError(e))
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.obra-layout {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 1.25rem;
  align-items: start;
}

.price {
  font-size: 1.35rem;
  font-weight: 700;
  color: #d97706;
  margin-bottom: 1rem;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}

.section-head .section-title {
  margin: 0;
}

.artist-chips {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.artist-chips li {
  padding: 0.65rem 0.85rem;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  font-size: 0.85rem;
}

.artist-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.artist-chips span {
  display: block;
  color: var(--text-muted);
  font-size: 0.78rem;
  margin-top: 0.15rem;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cert-panel,
.staff-panel {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: var(--radius);
  padding: 1.15rem;
}

.staff-panel {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.cert-empty {
  text-align: center;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
}

.cert-panel h3,
.staff-panel h3 {
  font-size: 0.95rem;
}

.cert-panel p {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.cert-panel span {
  display: block;
  font-size: 0.72rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.empty-hint {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

@media (max-width: 640px) {
  .obra-layout {
    grid-template-columns: 1fr;
  }
}
</style>
