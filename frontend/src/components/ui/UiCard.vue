<script setup lang="ts">
defineProps<{ title?: string; description?: string }>()
</script>

<template>
  <section class="rounded-lg border border-border bg-surface">
    <header
      v-if="title || $slots.actions"
      class="flex items-start justify-between gap-4 border-b border-border px-4 py-3"
    >
      <div>
        <h2 v-if="title" class="text-base font-semibold">{{ title }}</h2>
        <p v-if="description" class="mt-0.5 text-sm text-fg-muted">{{ description }}</p>
      </div>
      <slot name="actions" />
    </header>
    <div class="p-4">
      <slot />
    </div>
  </section>
</template>
