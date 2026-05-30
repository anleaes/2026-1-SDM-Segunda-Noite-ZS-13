<template>
  <div class="detail-banner" :class="`banner-${variant}`">
    <button type="button" class="back-btn" @click="$router.back()">← Voltar</button>
    <div class="banner-body">
      <span v-if="badge" class="banner-badge">{{ badge }}</span>
      <h1>{{ title }}</h1>
      <p v-if="meta">{{ meta }}</p>
    </div>
    <div v-if="$slots.actions" class="banner-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  meta: { type: String, default: '' },
  badge: { type: String, default: '' },
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'galeria', 'obra', 'exposicao'].includes(v),
  },
})
</script>

<style scoped>
.detail-banner {
  border-radius: var(--radius);
  padding: 1.25rem 1.35rem;
  margin-bottom: 1.25rem;
  color: #fff;
  position: relative;
}

.banner-galeria {
  background: linear-gradient(120deg, #059669, #10b981);
}

.banner-obra {
  background: linear-gradient(120deg, #d97706, #f59e0b);
}

.banner-exposicao {
  background: linear-gradient(120deg, #7c3aed, #a855f7);
}

.banner-default {
  background: linear-gradient(120deg, #2563eb, #3b82f6);
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.banner-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.25);
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.banner-body h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.banner-body p {
  opacity: 0.9;
  font-size: 0.9rem;
}

.banner-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
</style>
