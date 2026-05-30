<template>
  <div v-loading="loading" class="home-page">
    <PageHeader
      theme="home"
      icon="👋"
      :title="`Olá, ${auth.user?.first_name}!`"
      :subtitle="`Bem-vindo ao painel · ${auth.roleLabel}`"
    />

    <div class="quick-grid">
      <button
        v-for="item in stats"
        :key="item.label"
        type="button"
        class="quick-card"
        :class="item.color"
        @click="$router.push(item.route)"
      >
        <span class="quick-icon">{{ item.emoji }}</span>
        <span class="quick-value">{{ item.value }}</span>
        <span class="quick-label">{{ item.label }}</span>
        <span class="quick-go">Ver →</span>
      </button>
    </div>

    <div class="home-columns">
      <el-card shadow="never" class="home-about">
        <template #header>{{ auth.canManage ? 'Gestão do acervo' : 'Como usar o sistema' }}</template>
        <ol v-if="auth.canManage" class="steps">
          <li>Cadastre <router-link :to="{ name: 'galerias' }">galerias</router-link> e <router-link :to="{ name: 'exposicoes' }">exposições</router-link></li>
          <li>Registre <router-link :to="{ name: 'obras' }">obras</router-link> com categoria e certificado</li>
          <li>Vincule obras às exposições e artistas ao acervo</li>
          <li>Registre restaurações e gerencie o status das mostras</li>
        </ol>
        <ol v-else class="steps">
          <li>Explore <router-link :to="{ name: 'galerias' }">galerias</router-link> e suas exposições</li>
          <li>Consulte o <router-link :to="{ name: 'obras' }">acervo de obras</router-link></li>
          <li>Como visitante: compre ingressos e avalie exposições</li>
        </ol>
      </el-card>
      <el-card shadow="never" class="home-tip">
        <template #header>Dica</template>
        <p v-if="auth.canManage">
          Como {{ auth.roleLabel }}, use os botões <strong>+ Nova</strong> nas páginas de Galerias, Obras e Exposições
          para cadastrar conteúdo. O Django Admin também está disponível em
          <a href="http://localhost:8000/admin/" target="_blank" rel="noopener">localhost:8000/admin</a>.
        </p>
        <p v-else>
          Seu perfil está em <router-link :to="{ name: 'perfil' }">Minha conta</router-link> — edite dados, senha e veja suas atividades.
        </p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import { fetchDashboard } from '@/api/services'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const loading = ref(true)
const stats = ref([
  { label: 'Galerias', value: 0, route: { name: 'galerias' }, emoji: '🏛️', color: 'qc-green' },
  { label: 'Obras', value: 0, route: { name: 'obras' }, emoji: '🎨', color: 'qc-amber' },
  { label: 'Exposições', value: 0, route: { name: 'exposicoes' }, emoji: '📅', color: 'qc-purple' },
])

onMounted(async () => {
  try {
    const data = await fetchDashboard()
    stats.value[0].value = data.galerias
    stats.value[1].value = data.obras
    stats.value[2].value = data.exposicoes
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.quick-card {
  text-align: left;
  padding: 1.15rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: #fff;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}

.quick-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.qc-green { border-left: 4px solid #10b981; }
.qc-amber { border-left: 4px solid #f59e0b; }
.qc-purple { border-left: 4px solid #a855f7; }

.quick-icon { font-size: 1.5rem; display: block; margin-bottom: 0.35rem; }
.quick-value { font-size: 2rem; font-weight: 700; display: block; line-height: 1.1; }
.quick-label { font-size: 0.85rem; color: var(--text-muted); display: block; margin-top: 0.15rem; }
.quick-go { font-size: 0.75rem; color: var(--primary); margin-top: 0.5rem; display: block; }

.home-columns {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1rem;
}

.steps {
  padding-left: 1.25rem;
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.9;
}

.home-tip p {
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.6;
}

@media (max-width: 640px) {
  .quick-grid,
  .home-columns {
    grid-template-columns: 1fr;
  }
}
</style>
