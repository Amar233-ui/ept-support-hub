<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{ icon?: Component; title: string; description?: string }>()
</script>

<template>
  <div class="flex flex-col items-center justify-center px-6 py-12 text-center">
    <div
      v-if="icon"
      class="mb-4 flex size-10 items-center justify-center rounded-lg border border-border bg-surface text-fg-muted"
    >
      <component :is="icon" class="size-5" aria-hidden="true" />
    </div>
    <h3 class="text-md font-semibold">{{ title }}</h3>
    <p v-if="description" class="mt-1 max-w-sm text-base text-fg-muted">{{ description }}</p>
    <div v-if="$slots.default" class="mt-5 flex gap-2">
      <slot />
    </div>
  </div>
</template>
