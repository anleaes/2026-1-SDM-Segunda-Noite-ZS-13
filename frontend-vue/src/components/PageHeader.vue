<template>
  <header class="page-header" :class="`theme-${theme}`">
    <div v-if="icon" class="page-header-icon">{{ icon }}</div>
    <div class="page-header-text">
      <h1>{{ title }}</h1>
      <p v-if="subtitle">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.extra" class="page-header-extra">
      <slot name="extra" />
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
  theme: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'home', 'galerias', 'obras', 'exposicoes', 'perfil'].includes(v),
  },
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem 1.35rem;
  border-radius: var(--radius);
  margin-bottom: 1.35rem;
  border: 1px solid var(--border);
  background: #fff;
}

.page-header-icon {
  font-size: 2rem;
  line-height: 1;
  flex-shrink: 0;
}

.page-header-text h1 {
  font-size: 1.45rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}

.page-header-text p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.page-header-extra {
  margin-left: auto;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.theme-home {
  background: linear-gradient(135deg, #eff6ff 0%, #fff 60%);
  border-color: #bfdbfe;
}

.theme-galerias {
  background: linear-gradient(135deg, #ecfdf5 0%, #fff 55%);
  border-color: #a7f3d0;
}

.theme-obras {
  background: linear-gradient(135deg, #fef3c7 0%, #fff 55%);
  border-color: #fde68a;
}

.theme-exposicoes {
  background: linear-gradient(135deg, #fae8ff 0%, #fff 55%);
  border-color: #e9d5ff;
}

.theme-perfil {
  background: linear-gradient(135deg, #f1f5f9 0%, #fff 55%);
  border-color: #cbd5e1;
}

@media (max-width: 560px) {
  .page-header {
    flex-wrap: wrap;
  }

  .page-header-extra {
    margin-left: 0;
    width: 100%;
  }
}
</style>
