<script setup lang="ts">
import { SearchX } from '@lucide/vue'

import UiEmptyState from '@/components/ui/UiEmptyState.vue'
</script>

<template>
  <UiEmptyState
    :icon="SearchX"
    title="Page introuvable"
    description="Cette page n'existe pas ou a été déplacée."
  >
    <RouterLink
      to="/"
      class="inline-flex h-8 items-center rounded-md bg-accent px-3 text-base font-medium text-accent-fg hover:bg-accent-hover"
    >
      Retour à l'accueil
    </RouterLink>
  </UiEmptyState>
</template>
